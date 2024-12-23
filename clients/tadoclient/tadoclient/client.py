import asyncio
import time
from functools import lru_cache
from typing import Any, List, NamedTuple, get_args

import httpx
from tadoclient.exceptions import TadoAuthError, TadoClientError
from tadoclient.models import (
    TadoClientConfig,
    TadoToken,
    TadoWebHookEventType,
    User,
    WebHook,
    Zone,
    ZoneState,
)
from tadoclient.utils import is_token_expired


class TadoClient:
    @classmethod
    @lru_cache(maxsize=1000)
    def get_client(
        cls,
        token: TadoToken,
        config: TadoClientConfig,
    ) -> "TadoClient":
        return cls(token, config)

    def __init__(self, token: TadoToken, config: TadoClientConfig) -> None:
        self.token = token
        self.config = config
        self.api_base_url = config.api_base_url
        self._populated_user: User | None = None

    def _get_headers(self) -> dict[str, str]:
        if not self.token or is_token_expired(self.token):
            raise TadoAuthError("No valid token or token expired")
        if not self.token:
            raise TadoAuthError("No valid token available")

        return {"Authorization": f"Bearer {self.token.access_token}"}

    async def refresh_token(self) -> TadoToken:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config.refresh_token_url,
                data={
                    "grant_type": "refresh_token",
                    "client_id": self.config.client_id,
                    "client_secret": self.config.client_secret,
                    "refresh_token": self.token.refresh_token,
                },
            )
            if response.status_code != 200:
                raise TadoAuthError("Failed to refresh token")
            token_dict = response.json()

            token_dict["expires_at"] = int(
                token_dict.get("expires_in", 0) + time.time()
            )
            del token_dict["expires_in"]

            new_token = TadoToken(**token_dict)
            self.token = new_token
            return new_token

    async def get_user(self) -> User:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/me",
                headers=self._get_headers(),
            )
            if response.status_code != 200:
                raise TadoClientError("Failed to get user info")
            return User(**response.json())

    async def get_zones(self, home_id: int) -> list[Zone]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/homes/{home_id}/zones",
                headers=self._get_headers(),
            )
            if response.status_code != 200:
                raise TadoClientError("Failed to get zones")
            return [Zone(**zone) for zone in response.json()]

    async def get_zone_state(self, home_id: int, zone_id: int) -> ZoneState:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/homes/{home_id}/zones/{zone_id}/state",
                headers=self._get_headers(),
            )
            if response.status_code != 200:
                raise TadoClientError("Failed to get state")
            return ZoneState(**response.json())

    async def list_hooks(self, home_id: int) -> list[WebHook]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/homes/{home_id}/hooks",
                headers=self._get_headers(),
            )
            if response.status_code != 200:
                raise TadoClientError("Failed to list hooks")
            return [WebHook(**hook) for hook in response.json()]

    async def add_hook(self, home_id: int, url: str) -> WebHook:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/homes/{home_id}/hooks",
                headers=self._get_headers(),
                json={
                    "events": list(get_args(TadoWebHookEventType)),
                    "url": url,
                },
            )
            if response.status_code != 200:
                raise TadoClientError("Failed to add hook")
            return WebHook(**response.json())

    async def remove_hook(self, home_id: int, hook_id: int) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.api_base_url}/homes/{home_id}/hooks/{hook_id}",
                headers=self._get_headers(),
            )
            if response.status_code != 204:
                raise TadoClientError("Failed to remove hook")

    async def populated_user(self) -> User:
        if self._populated_user:
            # Returning cached user
            return self._populated_user

        user = await self.get_user()

        for home in user.homes:
            zones, webhooks = await asyncio.gather(
                self.get_zones(home.id), self.list_hooks(home.id)
            )
            zones = await self.get_zones(home.id)

            home.zones = zones
            home.webhooks = webhooks

            zone_states = await asyncio.gather(
                *[self.get_zone_state(home.id, zone.id) for zone in zones]
            )

            for zone, state in zip(zones, zone_states):
                zone.state = state

        self._populated_user = user
        return user
