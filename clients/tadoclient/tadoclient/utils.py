import time

from tadoclient.models import TadoToken


def is_token_expired(token: TadoToken | None) -> bool:
    if not token:
        return True
    exp = token.expires_at
    if not exp:
        return True
    print(exp, time.time())
    return exp < time.time()
