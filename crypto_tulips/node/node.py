"""
Module with node class and its functionality
"""
import socket
import pickle
from p2p import p2p_client, connection_manager

class Node:
    """
    A node in the network
    """

    def __init__(self, my_port):
        self.port = my_port
        self.connection_manager = None
        print('Started a node')

    def __del__(self):
        print('Ended node')

    @staticmethod
    def read_callback(data):
        """
        Temporary read callback
        """
        print('\t\t{}'.format(data))

    def join_network(self, bootstrap_host, bootstrap_port, peer_timeout=10, recv_data_size=1024, socket_timeout=10, read_callback=None):
        """
        Join the network and start communications

        Arguments:
        bootstrap_host -- host name of the bootstrap node
        bootstrap_port -- port of the bootstrap node
        peer_timeout=10 -- timeout on the peer before it is considered to be inactive
        recv_data_size=1024 -- default read size
        socket_timeout=10 -- timeout on socket recv
        read_callback=None -- callback to which redirect recv msgs
        """
        if read_callback is None:
            callback = Node.read_callback
        else:
            callback = read_callback
        known_peers = self.connect_to_bootstrap(host=bootstrap_host, port=bootstrap_port)
        self.connection_manager = connection_manager.ConnectionManager(server_port=self.port, \
                peer_timeout=peer_timeout, recv_data_size=recv_data_size, socket_timeout=socket_timeout)
        self.connection_manager.accept_connection(read_callback=callback, run_as_a_thread=True)
        for peer in known_peers:
            self.peer_connection(peer, read_callback=read_callback)

    def peer_connection(self, peer, read_callback=None):
        """
        Communication with a regular node during connection

        Arguments:
        peer -- peer to connect to
        read_callback=None -- callback to which redirect recv msgs
        """
        if read_callback is None:
            callback = Node.read_callback
        else:
            callback = read_callback
        self.connection_manager.connect_to(host=peer.ip_address, \
                port=int(peer.port), read_callback=callback)

    def connect_to_bootstrap(self, host, port):
        """
        Connect to the bootstrap node and get its known peers

        Arguments:
        host -- host address of the bootstrap node
        port -- port of the bootstrap node

        Return:
        list -- list of known Pp2p.p2p_peer.Peer
        """
        client = p2p_client.P2pClient()
        client.connect_to(host=host, port=port)
        host = socket.gethostname()
        client.send_msg(str(host) + ':' + str(self.port))
        recv_data = client.recv_msg(decode=False)
        known_peers = pickle.loads(recv_data)
        client.close_socket()
        return known_peers

    def close(self):
        """
        Clean up and end node
        """
        self.connection_manager.close_all()
