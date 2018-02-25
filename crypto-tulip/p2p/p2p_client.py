"""
Module with class with TCP client functionality for a peer
"""

import socket


class P2pClient:
    """
    Class that allows connection to a TCP server and exchange of messages
    """

    def __init__(self, data_size=1024):
        """
        Basic constructor.

        Arguments:
        data_size -- how much data to read at a time. The default is 1024
        """
        self.data_size = 1024
        self.sock = None
        self.host = None
        self.port = None
        self.__connected = False
        self.__socket_open = False

        self.__do_socket_creation()

        self.__connected = False
        self.data_size = data_size

    def __do_socket_creation(self):
        """
        Create socket
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket_open = True

    def set_timeout(self, timeout):
        """
        Set a timeout on the socket

        Arguments:
        timeout -- time to wait before getting timeout
        """
        self.sock.settimeout(timeout)

    def connect_to(self, host, port):
        """
        Make a connection to a given host.

        Arguments:
        host -- host's name
        port -- host's port

        Returns:
        bool -- was the connection successful
        """
        if self.__connected:
            self.close_socket()
        if not self.__socket_open:
            self.__do_socket_creation()
        self.host = host
        self.port = port
        try:
            self.sock.connect((self.host, self.port))
        except socket.error:
            print('Was not able to connect to server {}:{}'.format(self.host, self.port))
            success = False
        else:
            self.__connected = True
            success = True
        return success

    def send_msg(self, data, encode=True):
        """
        Send a message to the connected host

        Arguments:
        data -- data to send
        """
        if encode:
            send_data = data.encode()
        else:
            send_data = data
        self.sock.send(send_data)

    def recv_msg(self, decode=True):
        """
        Read msg from the host

        Returns:
        String that was read
        """
        data = self.sock.recv(self.data_size)
        if decode:
            return data.decode('utf-8')
        return data

    def close_socket(self):
        """
        Close opened socket
        """
        self.sock.close()
        self.__connected = False
        self.__socket_open = False
        self.host = None
        self.port = None
