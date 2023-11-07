from .code import utf8bencode, utf8bdecode
from hashlib import sha256
from base64 import urlsafe_b64encode

from logging import getLogger
log = getLogger(__name__)

__all__ = [
    'hashalgos',
    'mktarget',
]

hashalgos = {
    'sha256-base64url': lambda bs:
    urlsafe_b64encode(sha256(bs).digest()).rstrip(b'=').decode('utf8')
}


def mktarget(data):
    return data['basedir'] + '/' + \
        hashalgos[data['hashalgo']](utf8bencode(data))
