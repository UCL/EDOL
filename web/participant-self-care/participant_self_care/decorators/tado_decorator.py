import time
from collections.abc import Callable
from functools import wraps
from typing import Awaitable, ParamSpec, TypeVar

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from tadoclient.client import TadoClient
from tadoclient.exceptions import TadoAuthError
from tadoclient.models import TadoClientConfig, TadoToken

P = ParamSpec("P")
R = TypeVar("R")


def require_tado_auth(
    *, tado_config: TadoClientConfig, refresh_before: int = 300
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorator that handles Tado authentication and token refresh.

    Args:
        refresh_before: Number of seconds before token expiry to trigger refresh

    Adds tadoclient to the request object if authentication is successful.
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | RedirectResponse:
            # Find request object in args or kwargs
            request: object = next(
                (arg for arg in args if isinstance(arg, Request)),
                kwargs.get("request", None),
            )

            if not request:
                raise ValueError("No request object found in function arguments")

            if not isinstance(request, Request):
                raise ValueError("Request object is not of type Request")

            try:
                # Get token from session
                token = request.session.get("tado_token")
                if not token:
                    return RedirectResponse(url="/login")

                # Initialize TadoClient
                tadoclient = TadoClient.get_client(TadoToken(**token), tado_config)

                # Check if token needs refresh
                current_time = time.time()
                if tadoclient.token.expires_at - current_time < refresh_before:
                    try:
                        new_token = await tadoclient.refresh_token()
                        request.session["tado_token"] = new_token.model_dump()
                        # Reinitialize client with new token
                        tadoclient = TadoClient.get_client(new_token, tado_config)
                    except Exception as e:
                        raise TadoAuthError(f"Failed to refresh token: {str(e)}")

                # Add tadoclient to request state
                request.state.tadoclient = tadoclient

                # Call the original function
                return await func(*args, **kwargs)

            except TadoAuthError as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Authentication error: {str(e)}",
                )

        return wrapper

    return decorator
