from .code import utf8bencode, utf8bdecode, CodingError
from .validate import validate_request, ValidationError
from .authorize import authorize_request, AuthorizationError
from .action import enact_request
from socketserver import StreamRequestHandler, ThreadingUnixStreamServer, UnixStreamServer
from pathlib import Path
from shutil import chown

from logging import getLogger
log = getLogger(__name__)

__all__ = [
    'serve',
]

def serve(basedirs,
          socketpath,
          socketowner,
          socketgroup,
          socketperms,
          threaded=False):

    if not isinstance(socketpath, Path):
        socketpath = Path(socketpath)

    if threaded:
        Server = ThreadingUnixStreamServer
    else:
        Server = UnixStreamServer

    class Handler(StreamRequestHandler):
        def handle(self):
            try:
                log.debug('connection handler started')
                r = self.rfile.read()
                log.debug('request read as %s', repr(r))
                r = utf8bdecode(r)
                log.debug('request decoded to %s', repr(r))
                r = validate_request(r)
                log.debug('request validated')
                r = authorize_request(r)
                log.debug('request authorized')
                enact_request(r)
                log.debug('request enacted')
            except CodingError as error:
                log.warning('request could not be decoded: %s', error)
                response = {
                    'status': 'failure',
                    'reason': 'bad encoding',
                    'message': str(error),
                }
            except ValidationError as error:
                log.warning('request could not be validated: %s', error)
                response = {
                    'status': 'failure',
                    'reason': 'bad request',
                    'message': str(error),
                }
            except AuthorizationError as error:
                log.warning('request was denied authorization: %s', error)
                response = {
                    'status': 'failure',
                    'reason': 'authorization failure',
                    'message': str(error),
                }
            except Exception as error:
                log.error('request triggered an internal error: %s', error)
                response = {
                    'status': 'failure',
                    'reason': 'internal error',
                    'message': str(error),
                }
            else:
                log.info('request succeeded')
                response = {
                    'status': 'success',
                }
            finally:
                log.debug('sending response: %s', repr(response))
                self.wfile.write(utf8bencode(response))
                log.debug('response sent, connection handler finished')

    try:
        with Server(str(socketpath.absolute()), Handler, bind_and_activate=False) as s:
            # Create the socket file. Connection attempts are refused.
            log.debug('binding (creating) socket at %s', repr(s.server_address))
            s.server_bind()

            # Set permissions, and then owner and group of the socket
            log.debug('chmoding socket to %s', oct(socketperms))
            socketpath.chmod(socketperms)
            if socketowner or socketgroup:
                log.debug('chowning socket to owner %s and group %s', repr(socketowner), repr(socketgroup))
                chown(socketpath, socketowner, socketgroup)

            # Begin listening. Connections can now be accepted.
            log.debug('listening on socket')
            s.server_activate()

            # Handle requests
            log.debug('begin request loop')
            s.serve_forever()

    finally:
        log.debug('deleting socket')
        socketpath.unlink(missing_ok=True)
