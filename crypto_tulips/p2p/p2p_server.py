"""
Module with classes with TCP server functionality for a peer
"""

import socket
import ssl


class P2pClientPair:
    """
    Class that contains information returned from a connected client to a server
    """

    def __init__(self, sock, addr):
        """
        Construtor to initialize the class
        """
        self.socket = sock
        self.address = addr


class P2pServer:
    """
    Class that allows to listen to incomming TCP connections to exhcnage messages
    """
    keyfile = 'crypto_tulips/p2p/private.pem'
    certfile = 'crypto_tulips/p2p/cacert.pem'

    def __init__(self, port, data_size=1024, host=None):
        """
        Basic constructor.

        Arguments:
        data_size -- how much data to read at a time. The default is 1024
        """
        self.data_size = 1024
        self.sock = None
        self.host = None
        self.port = None
        self.__socket_open = False

        self.do_socket_creation()
        self.data_size = data_size
        if host is None:
            self.host = socket.gethostname()
        else:
            self.host = host
        self.port = port
        self.do_binding()

    def do_socket_creation(self):
        """
        Create socket
        """
        a_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock = ssl.wrap_socket(a_sock, server_side=True, \
                keyfile=self.keyfile, \
                certfile=self.certfile)

    def set_timeout(self, timeout, client_pair=None, client_socket=None):
        """
        Set timeout on the given socket

        Arguments:
        timeout -- time to wait before timeout
        client_pair -- P2pClientPair which socket to change
        client_socket -- client socket which socket to change
        """
        if client_pair is None:
            client_socket.settimeout(timeout)
        else:
            client_pair.socket.settimeout(timeout)

    def do_binding(self):
        """
        Bind socket to the server's host and port
        """
        self.sock.bind((self.host, self.port))
        self.__socket_open = True
        self.sock.listen(5)

    def accept_client(self):
        """
        Accept one client. Creates and binds socket if not done before.

        Returns:
        P2pClientPair -- a class that has accepted client's socket and ip address
        """
        if not self.__socket_open:
            self.do_socket_creation()
            self.do_binding()
        client_sock, client_addr = self.sock.accept()
        client_pair = P2pClientPair(client_sock, client_addr)
        return client_pair

    def send_msg(self, data, client_pair=None, client_socket=None, encode=True):
        """
        Sends a msg to a given client

        Arguments:
        data -- data to send to a client. Should be a string
        client_pair -- a P2pClientPair of a client that should receive the msg. Either client_pair or client_socket can be used
        client_socket -- socket of a client. Either client_pair or client_socket can be used
        """
        if client_pair is None:
            socket_to_use = client_socket
        else:
            socket_to_use = client_pair.socket
        if encode:
            send_data = data.encode()
        else:
            send_data = data
        socket_to_use.sendall(send_data)

    def recv_msg(self, client_pair=None, client_socket=None, decode=True):
        """
        Reads a msg from a given client

        Arguments:
        client_pair -- a P2pClientPair of a client that is expected to send us a msg. Either of arguments can be used
        client_socket -- socket of a client. Either of arguments can be used

        Returns:
        String representation of received msg
        """
        if client_pair is None:
            socket_to_use = client_socket
        else:
            socket_to_use = client_pair.socket
        data = self.recv_all(socket_to_use, self.data_size)
        if decode:
            return data.decode('utf-8')
        return data

    def recv_all(self, sock, data_read_length):
        """
        Method for socket to read all data
        """
        data = b''
        while True:
            part = sock.recv(data_read_length)
            data += part
            if len(part) < data_read_length:
                break
        return data

    def close_client(self, client_pair=None, client_socket=None):
        """
        Close given client's socket

        Arguments:
        client_pair -- a P2pClientPair of a client that is needed to be closed
        client_socket -- a socket that needs to be closed
        """
        if client_pair is None:
            client_socket.close()
        else:
            client_pair.socket.close()

    def close_socket(self):
        """
        Close server's socket
        """
        self.sock.close()
        self.__socket_open = False
