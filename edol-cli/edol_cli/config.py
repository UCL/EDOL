import logging
from pathlib import Path

import toml
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Config(BaseModel):
    debug: bool = False
    climate: dict = {}  # to be replaced by pydantic model provided by climate package
    vaillant: dict = {}  # to be replaced by pydantic model provided by vaillant package

    def __init__(self, config_toml_path: Path | None = None):
        super().__init__()
        if not config_toml_path:
            config_toml_path = Path("edol-config.toml")

        if not config_toml_path.exists():
            logger.warning(
                f"Config file not found at {config_toml_path}. Using default settings."
            )
            logger.debug(f"Loading config from {config_toml_path}")
            return

        toml_data = toml.load(config_toml_path)
        self.debug = toml_data.get("debug", False)
        self.climate = toml_data.get("climate", {})
        self.vaillant = toml_data.get("vaillant", {})
