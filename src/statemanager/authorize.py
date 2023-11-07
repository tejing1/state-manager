from logging import getLogger
log = getLogger(__name__)

__all__ = [
    'AuthorizationError',
    'authorize_request',
]

class AuthorizationError(Exception):
    pass

def authorize_request(request):
    return request
