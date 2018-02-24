"""
Module containing bootstrap functionality
"""
import threading
import pickle
from p2p import p2p_server, p2p_peer

class BootstrapNode:
    """
    Class to work as a bootstrap node and be an entry point to the network
    """

    def __init__(self, port, data_size=1024):
        self.server = p2p_server.P2pServer(port=port, data_size=data_size)
        self.peer_list = []
        self.thread_list = []
        print('Created BootstrapNode')

    def close(self):
        """
        Clean up BootstrapNode before removing it
        """
        for a_thread in self.thread_list:
            a_thread.join()
        self.server.close_socket()

    def __del__(self):
        print('Length of peer list is {}'.format(len(self.peer_list)))
        print('BootstrapNode ended')

    def accept(self):
        """
        Accept regular node to add to the peer list and to provide it
        with current list of known peers
        """
        client_pair = self.server.accept_client()
        a_thread = threading.Thread(target=self.communication, args=(client_pair,))
        self.thread_list.append(a_thread)
        a_thread.start()

    def communication(self, client_pair):
        """
        Thread method to will exchange msgs with a regular node

        Arguments:
        client_pair -- The result of accepting client from the server
        """
        connection_info = self.server.recv_msg(client_pair=client_pair)
        # incomming msg should be in the format '127.0.0.1:25255'
        ip_addr, port = connection_info.split(':')
        # serialize current peer list and send it to the peer
        pickled_list = pickle.dumps(self.peer_list)
        self.server.send_msg(pickled_list, client_pair=client_pair, encode=False)
        # save peer to the peer list
        peer = p2p_peer.Peer(ip_address=ip_addr, port=port, mode=p2p_peer.PeerMode.Unknown)
        self.peer_list.append(peer)
        self.server.close_client(client_pair=client_pair)
