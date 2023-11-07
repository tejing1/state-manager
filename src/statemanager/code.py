from fastbencode import bdecode, bencode

from logging import getLogger
log = getLogger(__name__)

__all__ = [
    'CondingError',
    'utf8bencode',
    'utf8bdecode',
]

class CodingError(Exception):
    pass

def recursivestringmod(func, data):
    if type(data) == bytes or type(data) == str:
        return func(data)
    elif type(data) == int:
        return data
    elif type(data) == list:
        return [recursivestringmod(func, e) for e in data]
    elif type(data) == dict:
        return {func(k): recursivestringmod(func, v) for k, v in data.items()}
    else:
        raise CodingError('Unexpected type')


def utf8bencode(data):
    try:
        data = recursivestringmod(lambda s: s.encode('utf8'), data)
    except Exception as error:
        raise CodingError('recursive utf8 encoding failed') from error

    try:
        data = bencode(data)
    except Exception as error:
        raise CodingError('bencoding failed') from error

    return data


def utf8bdecode(data):
    try:
        data = bdecode(data)
    except Exception as error:
        raise CodingError('bdecoding failed') from error

    try:
        data = recursivestringmod(lambda s: s.decode('utf8'), data)
    except Exception as error:
        raise CodingError('recursive utf8 decoding failed') from error

    return data
