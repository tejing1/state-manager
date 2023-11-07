from subprocess import run

from logging import getLogger
log = getLogger(__name__)

__all__ = [
    'enact_request',
]

def enact_request(request):
    match request['action']:
        case 'link':
            command = ['ln', '-s', '--', request['source'], request['target']]
            run(command, check=True)
        case _:
            raise Exception(f'unsupported action: {request["action"]}')
