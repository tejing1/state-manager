from .hash import hashalgos, mktarget
from schema import Schema, SchemaError, And, Optional

from logging import getLogger
log = getLogger(__name__)

__all__ = [
    'ValidationError'
    'validate_hashed',
    'validate_target',
    'validate_request',
]

class ValidationError(Exception):
    pass

def validate_hashed(hashed):
    try:
        Schema({
            'basedir': str,
            'hashalgo': str,
            'type': 'simple',
            'nonce': str,
        }).validate(hashed)
        Schema({
            # FIXME: validate basedir more carefully. disallow trailing
            # '/' in particular
            'basedir': str,
            # Must have a 'hashalgo' key containing a string matching one
            # of our actual implementations
            'hashalgo': And(
                str,
                lambda algo: algo in hashalgos
            ),
            # Accept other keys unconditionally
            Optional(str): object,
        }).validate(hashed)
    except SchemaError as error:
        raise ValidationError from error
    return hashed

def validate_target(hashed, target):
    validate_hashed(hashed)
    try:
        Schema(mktarget(hashed)).validate(target)
    except SchemaError as error:
        raise ValidationError from error

def validate_request(request):
    try:
        Schema({
            'version': 1,
            'action': 'link',
            'hashed': dict,
            'target': str,
            'source': str,
        }).validate(request)
    except SchemaError as error:
        raise ValidationError from error
    validate_target(request['hashed'], request['target'])
    return request
