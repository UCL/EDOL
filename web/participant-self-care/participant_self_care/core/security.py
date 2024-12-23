import os
from functools import lru_cache

from cryptography.fernet import Fernet


@lru_cache()
def get_cipher() -> Fernet:
    key = os.getenv("EDOL_PP_SELF_CARE_ENCRYPTION_KEY")
    if key is None:
        raise ValueError("No EDOL_PP_SELF_CARE_ENCRYPTION_KEY set for FastAPI app")
    return Fernet(key)
