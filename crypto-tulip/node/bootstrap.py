"""
Module containing bootstrap functionality
"""
import threading
import pickle
import socket
from p2p import p2p_server, p2p_peer, p2p_client

class BootstrapNode:
    """
    Class to work as a bootstrap node and be an entry point to the network
    """

    def __init__(self, port, data_size=1024):
        self.data_size = data_size
        self.port = port
        self.server = p2p_server.P2pServer(port=port, data_size=data_size)
        self.peer_list = []
        self.thread_list = []
        self.run = True
        self.accepting_thread_running = False
        print('Created BootstrapNode')

    def close(self):
        """
        Clean up BootstrapNode before removing it
        """
        self.run = False
        if self.accepting_thread_running:
            self.unblock_accept()
        for a_thread in self.thread_list:
            a_thread.join()
        print('All threads are joined')
        self.server.close_socket()

    def __del__(self):
        print('Length of peer list is {}'.format(len(self.peer_list)))
        print('BootstrapNode ended')

    def accept(self, run_as_a_thread=False):
        """
        Accept regular node to add to the peer list and to provide it
        with current list of known peers
        """
        if run_as_a_thread:
            a_thread = threading.Thread(target=self.accepting_thread)
            self.thread_list.append(a_thread)
            a_thread.start()
            self.accepting_thread_running = True
        else:
            self.accept_one()

    def accepting_thread(self):
        """
        Thread method that accepst nodes until boostrap node is closed
        """
        print('Started accepting thread')
        while self.run:
            self.accept_one()
        print('Ended accepting thread')

    def accept_one(self):
        """
        Accept regular node to add to the peer list and to provide it
        with current list of known peers
        """
        client_pair = self.server.accept_client()
        a_thread = threading.Thread(target=self.communication, args=(client_pair,))
        self.thread_list.append(a_thread)
        a_thread.start()

    def unblock_accept(self):
        """
        Unblock running accepting thread
        """
        client = p2p_client.P2pClient(data_size=self.data_size)
        host = socket.gethostname()
        port = self.port
        client.connect_to(host, port)
        client.send_msg('')
        client.close_socket()


    def communication(self, client_pair):
        """
        Thread method to will exchange msgs with a regular node

        Arguments:
        client_pair -- The result of accepting client from the server
        """
        connection_info = self.server.recv_msg(client_pair=client_pair)
        if ':' not in connection_info:
            print('Ignoring connection, did not provide correct first msg format, {}'.format(connection_info))
            return
        # incomming msg should be in the format '127.0.0.1:25255'
        ip_addr, port = connection_info.split(':')
        # serialize current peer list and send it to the peer
        pickled_list = pickle.dumps(self.peer_list)
        self.server.send_msg(pickled_list, client_pair=client_pair, encode=False)
        # save peer to the peer list
        peer = p2p_peer.Peer(ip_address=ip_addr, port=port, mode=p2p_peer.PeerMode.Unknown)
        exists = self.check_peer_duplicate(ip_addr, port)
        if not exists:
            self.peer_list.append(peer)
            self.server.close_client(client_pair=client_pair)

    def check_peer_duplicate(self, ip_addr, port):
        """
        Check if given peer already exists in the list of peers

        Arguments:
        ip -- ip of the peer
        port -- port of the peer

        Returns
        bool -- is peer already in the list
        """
        exists = False
        for peer in self.peer_list:
            if peer.ip_address == ip_addr and peer.port == port:
                exists = True
                break
        return exists
