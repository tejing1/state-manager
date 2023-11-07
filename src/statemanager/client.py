from .hash import utf8bencode, utf8bdecode
from socket import socket, AF_UNIX, SOCK_STREAM, SHUT_WR

from logging import getLogger
log = getLogger(__name__)

__all__ = [
    'send_request',
]

def send_request(socketpath, request):
    with socket(AF_UNIX, SOCK_STREAM) as s:
        # Open the socket
        s.connect(socketpath)

        # Send request
        s.sendall(utf8bencode(request))

        # Close write side of connection
        s.shutdown(SHUT_WR)

        # Read until end of stream
        data = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk

        return utf8bdecode(data)
