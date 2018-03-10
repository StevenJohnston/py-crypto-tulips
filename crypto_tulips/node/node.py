"""
Module with node class and its functionality
"""
import socket
import pickle
from crypto_tulips.p2p import p2p_client, connection_manager
from crypto_tulips.node.bootstrap import BootstrapNode

class Node:
    """
    A node in the network
    """

    def __init__(self, my_port):
        self.port = my_port
        self.connection_manager = None
        self.host = None
        self.bootstrap_node = None
        self.bootstrap_node_running = False
        #print('Started a node')

    def start_bootstrap(self, port=25252):
        """
        Start a bootstrap node together with a regular node

        Arguments"
        port=25252 -- port on which to run a bootstrap node
        """
        if not self.bootstrap_node_running:
            self.bootstrap_node = BootstrapNode(port=port)
            self.bootstrap_node.accept(True)
            self.bootstrap_node_running = True

    def __del__(self):
        #print('Ended node')
        pass

    @staticmethod
    def read_callback(data):
        """
        Temporary read callback
        """
        print('\n\t\t{}'.format(data))

    def make_silent(self, silent):
        self.connection_manager.silent = silent

    def join_network(self, bootstrap_host, bootstrap_port=25252, peer_timeout=10, recv_data_size=1024, \
            socket_timeout=10, read_callback=None, wallet_callback=None, start_bootstrap=False):
        """
        Join the network and start communications

        Arguments:
        bootstrap_host -- host name of the bootstrap node
        bootstrap_port -- port of the bootstrap node
        peer_timeout=10 -- timeout on the peer before it is considered to be inactive
        recv_data_size=1024 -- default read size
        socket_timeout=10 -- timeout on socket recv
        read_callback=None -- callback to which redirect recv msgs
        wallet_callback=None -- callback to which redirect wallet connection
        start_bootstrap=False -- do we need to start a bootstrap node
        """
        if not self.bootstrap_node_running and start_bootstrap:
            self.start_bootstrap()
        if read_callback is None:
            callback = Node.read_callback
        else:
            callback = read_callback
        known_peers = self.connect_to_bootstrap(host=bootstrap_host, port=bootstrap_port)
        self.connection_manager = connection_manager.ConnectionManager(server_port=self.port, \
                peer_timeout=peer_timeout, recv_data_size=recv_data_size, socket_timeout=socket_timeout)
        self.connection_manager.accept_connection(read_callback=callback, run_as_a_thread=True, wallet_callback=wallet_callback)
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
        if self.host == peer.ip_address and self.port == int(peer.port):
            return
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
        host = socket.gethostbyname(socket.getfqdn())
        self.host = host
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
        if self.bootstrap_node_running:
            self.bootstrap_node.close()
