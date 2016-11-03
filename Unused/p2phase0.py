import asyncore, socket
import logging
from cStringIO import StringIO
from urlparse import urlparse

def make_request(req_type, what, details, ver="1.1"):
    """ Compose an HTTP request """
    NL = "\r\n"
    req_line = "{verb} {w} HTTP/{v}".format(
        verb=req_type, w=what, v=ver
    )
    details = [
        "{name}: {v}".format(name=n,v=v) for (n,v) in details.iteritems()
    ]
    detail_lines = NL.join(details)
    full_request = "".join([req_line, NL, detail_lines, NL, NL])
    return full_request
def parse_url(url, DEFAULT_PORT=80):
    """ Parse a given url into host, path, and port.
        Use DEFAULT_PORT (80) if unspecified.
    """
    parsed_url = urlparse(url)
    host, path, port = (parsed_url.hostname,
                        parsed_url.path,
                        parsed_url.port)
    if not port:
        port = DEFAULT_PORT
    return (host, path, port)

class HTTPClient(asyncore.dispatcher):
    ## Size of the buffer for each recv
    RECV_CHUNK_SIZE = 8192

    def __init__(self, url):
        asyncore.dispatcher.__init__(self)
        host, path, port = parse_url(url)

        # Create a logger
        self.logger = logging.getLogger(url)

        # Create a TCP socket to host at the right port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

        self.host = host

        # Create recv buffer and send buffer
        (self.recvbuf, self.sendbuf) = (StringIO(), "")

        # Make an initial request & deliver it
        request = make_request('GET', path,
            {'Host': host,
             'Connection': 'close'}
        )
        self.write(request)

    def write(self, data):
        """ Schedule to deliver data over the socket """
        self.sendbuf += data

    def handle_connect(self):
        self.logger.debug("Connected")

    def handle_close(self):
        self.logger.debug("Disconnected")
        self.close()

    def writeable(self):
        """ Check if there is anything to send """
        return len(self.sendbuf) > 0

    def handle_write(self):
        bytes_sent = self.send(self.sendbuf)
        self.sendbuf = self.sendbuf[bytes_sent:]

    def handle_read(self):
        recv_bytes = self.recv(HTTPClient.RECV_CHUNK_SIZE)
        self.logger.debug("recvd {} bytes".format(len(recv_bytes)))
        self.recvbuf.write(recv_bytes)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
        format="%(asctime)-15s %(name)s: %(message)s"
    )
    clients = [
        HTTPClient("http://pantip.com/"),
        HTTPClient("http://www.muic.mahidol.ac.th/eng/"),
        HTTPClient("http://www.nytimes.com/"),
        HTTPClient("http://www.cnn.com/"),
    ]
    asyncore.loop()