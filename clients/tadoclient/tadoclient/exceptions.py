class TadoClientError(Exception):
    """Base exception for TadoClient"""
    pass

class TadoAuthError(TadoClientError):
    """Authentication related errors"""
    pass
