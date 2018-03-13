"""
Module with classes to store information about a peer
"""

from enum import Enum
import time

class PeerMode(Enum):
    """
    Enumerator to specify how the peer got connected to.
    Client peers are peers we have connected to.
    Server peers are peers that have connected to us.
    """
    Client = 2
    Server = 1
    Unknown = 0


class Peer:
    """
    Peer class that stores information about a peer required to communicate with that peer
    """

    def __init__(self, socket=None, ip_address=None, port=None, mode=None):
        """
        Initializer for a Peer.

        Arguments:
        socket -- open socket of a peer
        ip_address -- ip address of the peer
        port -- port of the peer
        mode -- a PeerMode instance to specify how peer got connected to
        """
        self.socket = None
        self.ip_address = None
        self.port = None
        self.mode = None
        self.last_message_time = None

        self.socket = socket
        self.ip_address = ip_address
        self.port = port
        self.mode = mode
        self.last_message_time = None

    def make_timestamp(self):
        """
        Give peer's last_message_time timestamp
        """
        self.last_message_time = time.time()

    def get_ip_address(self):
        """
        In server mode when we store a pair of
        ip and port of connected client, which
        means that we need to tream them differently based on the mode

        Returns:
        string -- ip address
        """
        if self.mode == PeerMode.Server:
            return self.ip_address[0]
        return self.ip_address

    def give_time_difference(self):
        """
        Return the difference between current time and the last_message_time of a peer
        """
        current_time = time.time()
        return current_time - self.last_message_time
