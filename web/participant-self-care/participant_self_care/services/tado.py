from authlib.integrations.starlette_client import OAuth
from participant_self_care.core.config import config

tado_oauth = OAuth()
tado_oauth.register(**config.tado.model_dump())
