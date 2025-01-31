import base64
import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Literal

import dotenv
import requests
import toml
from pydantic import BaseModel
from vaillant.schemas import (
    SystemSettingsResponse,
    TokenErrorResponse,
    TokenResponse,
    VaillantApiException,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

dotenv.load_dotenv()

VAILLANT_API_ENDPOINT_ROOT = os.getenv(
    "VAILLANT_API_ENDPOINT_ROOT", "https://api.vaillant-group.com"
)


class VaillantApiConfig(BaseModel):
    token_endpoint: str = f"{VAILLANT_API_ENDPOINT_ROOT}/uaa/oauth/token"
    consumption_endpoint: str = (
        f"{VAILLANT_API_ENDPOINT_ROOT}/service-connected-control/consumption-api/v1/systems"
    )
    settings_endpoint: str = (
        f"{VAILLANT_API_ENDPOINT_ROOT}/service-connected-control/settings-api/v1/systems"
    )

    topology_endpoint: str = (
        f"{VAILLANT_API_ENDPOINT_ROOT}/service-connected-control/systems-api/v2/systems"
    )

    contract_systems_endpoint: str = (
        f"{VAILLANT_API_ENDPOINT_ROOT}/service-connected-control/system-registration-api-with-consent/v1/contracts"
    )

    client_id: str = os.getenv("VAILLANT_API_CLIENT", "")
    client_secret: str = os.getenv("VAILLANT_API_SECRET", "")
    # get this from https://developer.vaillant-group.com/profile
    subscription_key: str = os.getenv("VAILLANT_API_SUBSCRIBTION_KEY", "")
    contract_number: str = os.getenv("VAILLANT_API_CONTRACT_NUMBER", "")

    def load_from_toml(self, path: str) -> None:
        with open(path) as f:
            data = toml.load(f)

            # If the client_id is not provided in the config file, we will use the default value
            if "client_id" in data:
                self.client_id = data["client_id"]

            if "client_secret" in data:
                self.client_secret = data["client_secret"]

            if "subscription_key" in data:
                self.subscription_key = data["subscription_key"]

            if "contract_number" in data:
                self.contract_number = data["contract_number"]

            if (
                not self.client_id
                or not self.client_secret
                or not self.subscription_key
                or not self.contract_number
            ):
                raise ValueError(
                    "Client ID, Client Secret, Subscription Key, and Contract Number must be provided in the config file or as environment variables"
                )


class VaillantApi:
    def __init__(self, config: VaillantApiConfig, serials: List[str]) -> None:
        if not isinstance(config, VaillantApiConfig):
            raise TypeError("config must be an instance of VaillantApiConfig")

        if not isinstance(serials, List):
            raise TypeError("serials must be a list")

        if not all(isinstance(serial, str) for serial in serials):
            raise TypeError("serials must be a list of strings")

        self._config = config
        self._serials: List[str] = serials
        self._token = None

    def _request(
        self, url: str, method: Literal["GET", "POST"] = "GET", data: dict = None
    ) -> requests.Response:
        token = self.get_token()

        headers = {
            "Content-Type": (
                "application/json"
                if method == "POST"
                else "application/x-www-form-urlencoded"
            ),
            "Authorization": f"Bearer {token}",
            "Ocp-Apim-Subscription-Key": self._config.subscription_key,
        }

        request_params = {
            "method": method,
            "url": url,
            "headers": headers,
            "data": json.dumps(data) if method == "POST" else None,
        }

        try:
            response = requests.request(**request_params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.debug(response.text)

            raise VaillantApiException(
                TokenErrorResponse(error="request_failed", error_description=str(e))
            )

    def get_token(self) -> str:
        """
        Get the access token for the API
        Documentation here: https://developer.vaillant-group.com/api-specs#api=authorization_server&operation=create-access-token

        """
        # FIXME: this is insecure; remove it later
        if os.path.exists("access_token.txt"):
            last_modified = os.path.getmtime("access_token.txt")
            if datetime.now().timestamp() - last_modified < 3600:
                logger.debug("Token in the file is still valid")
                logger.warning("Using the token from the file")
                with open("cache/access_token.txt", "r") as f:
                    return f.read()

        if self._token and self._token.expires_at > datetime.now().timestamp():
            logger.debug("Token is still valid")
            return self._token.access_token

        # FIXME: refresh token in't used because the documentation doesn't mention it

        b64encoded_user_pass = base64.b64encode(
            f"{self._config.client_id}:{self._config.client_secret}".encode()
        ).decode()

        request_params = {
            "method": "POST",
            "url": self._config.token_endpoint,
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {b64encoded_user_pass}",
                "Ocp-Apim-Subscription-Key": self._config.subscription_key,
            },
            "data": {
                "grant_type": "client_credentials",
            },
        }

        response = requests.request(**request_params)
        try:
            token = TokenResponse(**response.json())
            token.expires_at = token.expires_in + datetime.now().timestamp()

            self._token = token

            # FIXME: remove this insecure code
            with open("cache/access_token.txt", "w") as f:
                f.write(token.access_token)

            return token.access_token
        except Exception as e:
            raise VaillantApiException(
                TokenErrorResponse(
                    error="token_request_failed", error_description=str(e)
                )
            )

    def get_components_consumption(
        self,
        serial: str,
        scale: Literal["hourly", "daily", "monthly"] = "hourly",
        from_datetime: datetime = datetime.now() - timedelta(days=1),
        to_datetime: datetime = datetime.now(),
    ) -> None:
        """
        Get consumption data of all system components in a system
        Shows for the selected time period the total consumption and the consumptions, fanned out for all known components (e.g. heat pump, boiler) within a system.

        Confer with consumption explanation in Endpoint `Get consumption data of a system`.
        https://developer.vaillant-group.com/api-specs#api=consumption_api&operation=get-consumption-for-system-components
        """
        timestamp_from = int(from_datetime.replace(microsecond=0).timestamp())
        timestamp_to = int(to_datetime.replace(microsecond=0).timestamp())

        url = f"{self._config.consumption_endpoint}/{serial}/system-components/consumption?scale={scale}&from={timestamp_from}&to={timestamp_to}"
        response = self._request(url, method="GET")
        with open(f"cache/sys_cons_{serial}.json", "w") as f:
            f.write(response.text)

    def get_single_consumption(
        self,
        serial: str,
        scale: Literal["hourly", "daily", "monthly"] = "hourly",
        from_datetime: datetime = datetime.now() - timedelta(days=1),
        to_datetime: datetime = datetime.now(),
    ) -> None:
        """
        Get consumption data of a system.

        Shows consumptions for the selected time period for central heating, cooling, hot water and solar yield in relation to the entire system.


        https://developer.vaillant-group.com/api-specs#api=consumption_api&operation=get-consumption-for-system
        """
        timestamp_from = int(from_datetime.replace(microsecond=0).timestamp())
        timestamp_to = int(to_datetime.replace(microsecond=0).timestamp())

        url = f"{self._config.consumption_endpoint}/{serial}/consumption?scale={scale}&from={timestamp_from}&to={timestamp_to}"
        response = self._request(url, method="GET")

        # FIXME: impelement the response parsing
        with open(f"cache/single_cons_{serial}.json", "w") as f:
            f.write(response.text)

    def get_components_consumption(
        self,
        serial: str,
        scale: Literal["hourly", "daily", "monthly"] = "hourly",
        from_datetime: datetime = datetime.now() - timedelta(days=1),
        to_datetime: datetime = datetime.now(),
    ) -> None:
        """
        Get the consumption for the given serial
        "https://api.vaillant-group.com/service-connected-control/consumption-api/v1/systems/${serialNumber}/system-components/consumption?scale=hourly[&from][&to]"
        """
        timestamp_from = int(from_datetime.replace(microsecond=0).timestamp())
        timestamp_to = int(to_datetime.replace(microsecond=0).timestamp())

        url = f"{self._config.consumption_endpoint}/{serial}/system-components/consumption?scale={scale}&from={timestamp_from}&to={timestamp_to}"
        response = self._request(url, method="GET")
        # FIXME: impelement the response parsing
        with open(f"cache/sys_cons_{serial}.json", "w") as f:
            f.write(response.text)

    def get_system_settings(
        self, system_id: str, include_metadata: bool = True
    ) -> SystemSettingsResponse:
        """
        Get system settings for the given system ID.
        """
        url = f"{self._config.settings_endpoint}/{system_id}?includeMetadata={str(include_metadata).lower()}"
        response = self._request(url, method="GET")

        # FIXME: impelement the response parsing
        # e.g. SystemSettingsResponse(**response.json())
        with open(f"cache/sys_set_{system_id}.json", "w") as f:
            f.write(response.text)

    def get_topology(self, serial: str) -> None:
        """
        Get the topology for the given serial
        https://developer.vaillant-group.com/api-specs#api=systems-api-v2&operation=get-hvac-system-topology
        """
        url = f"{self._config.topology_endpoint}/{serial}"
        response = self._request(url, method="GET")
        # FIXME: impelement the response parsing
        with open(f"cache/topology_{serial}.json", "w") as f:
            f.write(response.text)

    def get_contract_systems(self) -> None:
        """
        Get the contract systems
        """
        contract_number = self._config.contract_number

        url = f"{self._config.contract_systems_endpoint}/{contract_number}/systems"
        response = self._request(url, method="GET")

        # FIXME: impelement the response parsing
        with open(f"cache/contract_systems_{contract_number}.json", "w") as f:
            f.write(response.text)

    def register_client(self, serial: str, email: str, country: str = "GB") -> None:
        """
        Register a client
        """
        contract_number = self._config.contract_number

        url = f"{self._config.contract_systems_endpoint}/{contract_number}/systems"

        response = self._request(
            url,
            method="POST",
            data={"serialNumber": serial, "email": email, "country": country},
        )

        # FIXME: impelement the response parsing
        with open(f"register_client_{response.status_code}_{serial}.json", "w") as f:
            f.write(response.text)
