import os
from functools import cached_property
from pathlib import Path

import structlog
from tadoclient.models import TadoClientConfig
import toml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Config(BaseModel):
    debug: bool = Field(default=False)
    refresh: bool = Field(default=False)

    def load_from_config_toml(self, config_path: Path) -> None:
        with open(config_path, "r") as config_file:
            config = toml.load(config_file)
            self.logger.debug("Loaded config", config=config)

    @cached_property
    def logger(self) -> structlog.BoundLogger:
        logger: structlog._generic.BoundLogger = structlog.get_logger()
        return logger

    @cached_property
    def edol_pp_self_care_sess_secret(self) -> str:
        value = os.getenv("EDOL_PP_SELF_CARE_SESS_SECRET", None)
        if value is None:
            raise ValueError("No EDOL_PP_SELF_CARE_SESS_SECRET set for FastAPI app")
        return value

    @cached_property
    def database_url(self) -> str:
        value = os.getenv("DATABASE_URL", None)
        if value is None:
            raise ValueError(
                "No DATABASE_URL set for FastAPI app. E.g. sqlite+aiosqlite:///./users.sqlite"
            )
        return value

    @cached_property
    def tado(self) -> TadoClientConfig:
        return TadoClientConfig(
            client_id=os.getenv("TADO_CLIENT_ID"),
            client_secret=os.getenv("TADO_CLIENT_SECRET"),
            api_base_url=os.getenv("TADO_API_BASE_URL"),
            refresh_token_url=os.getenv("TADO_REFRESH_TOKEN_URL"),
            redirect_uri=os.getenv("TADO_REDIRECT_URI"),
            authorize_url=os.getenv("TADO_AUTHORIZE_URL"),
            access_token_url=os.getenv("TADO_TOKEN_URL"),
        )


"""Settings instance for the project."""
config = Config()
