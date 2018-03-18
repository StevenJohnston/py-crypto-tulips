"""
Module with node class and its functionality
"""
import socket
import pickle
import threading
import time
import json
from crypto_tulips.p2p import p2p_client, connection_manager, p2p_server, p2p_peer, message
from crypto_tulips.node.bootstrap import BootstrapNode
from crypto_tulips.services import block_service


class Node:
    """
    A node in the network
    """

    def __init__(self):
        self.connection_manager = None
        self.host = None
        self.bootstrap_node = None
        self.bootstrap_node_running = False
        self.gossip_port = 14141
        self.gossiping_run = False
        self.gossiping_timeout = 10
        self.gossip_threads = []
        self.default_bootstrap_port = 25252
        self.default_node_port = 36363
        self.port = self.default_node_port
        self.doing_blockchain_sync = False
        self.block_queue = []
        self._do_block_sync = True
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
        """
        Set silent mode on connection manager for this node

        Arguments:
        silent -- True to set silent mode, False to unset it
        """
        self.connection_manager.silent = silent

    def gossiping_listen(self):
        """
        Method to constantly listen to gossip connections and
        tell them about known peers
        """
        mini_server = p2p_server.P2pServer(self.gossip_port)
        while self.gossiping_run:
            client_pair = mini_server.accept_client()
            copy_list = []
            # creating new list of known peers because we only
            # need ip and port. Also, we cannot pickle socket object
            for peer in self.connection_manager.peer_list:
                new_peer = p2p_peer.Peer(ip_address=peer.get_ip_address(), port=self.default_node_port)
                copy_list.append(new_peer)
            pickled_list = pickle.dumps(copy_list)
            mini_server.send_msg(data=pickled_list, client_pair=client_pair, encode=False)
            mini_server.close_client(client_pair=client_pair)

    def unblock_gossiping_listen(self):
        """
        Method to unblock listening part of gossiping
        """
        mini_client = p2p_client.P2pClient()
        mini_client.connect_to(self.host, self.gossip_port)
        # don't care about what we receive, because we are going to exit anyway
        mini_client.recv_msg(decode=False)
        mini_client.close_socket()

    def gossiping_connect(self, read_callback):
        """
        Main gossiping method that connects to the peer and gets their known peers.
        After connecting it checks what peers current node is not connected to and does the
        connection.

        Arguments:
        read_callback -- callback which to call when we recv a msg from a new peer
        """
        new_peers = []
        for peer in self.connection_manager.peer_list:
            mini_client = p2p_client.P2pClient()
            peer_ip_address = peer.get_ip_address()
            # need to catch exceptions because peer might be closed
            try:
                mini_client.connect_to(peer_ip_address, self.gossip_port)
                pickled_list = mini_client.recv_msg(decode=False)
                new_known_peers = pickle.loads(pickled_list)
                mini_client.close_socket()
            except:
                mini_client.close_socket()
                continue
            for a_new_peer in new_known_peers:
                found_new = True
                # checking if any of current peers has the same ip
                # as each of new received peers
                # this specific new peer does not have its ip in peer list
                # we should connect to it
                for an_old_peer in self.connection_manager.peer_list:
                    an_old_peer_ip_address = an_old_peer.get_ip_address()
                    if a_new_peer.ip_address == an_old_peer_ip_address:
                        found_new = False
                        break
                if found_new:
                    # need to also check if current peer is our ip
                    if a_new_peer.ip_address != self.host:
                        already_added = False
                        # check if we already know about the peer
                        for a_new_peer_to_add in new_peers:
                            if a_new_peer.ip_address == a_new_peer_to_add.ip_address:
                                already_added = True
                                break
                        if not already_added:
                            new_peers.append(a_new_peer)
        for new_peer in new_peers:
            self.peer_connection(peer=new_peer, read_callback=read_callback)

    def gossiping_connect_thread(self, read_callback):
        """
        Thread method to connect to other peers gossip servers and get their known peers

        Arguments:
        read_callback -- callback to which redirect msg from newly connected peers
        """
        gossip_sleep = 1
        number_of_sleep_to_run = self.gossiping_timeout / gossip_sleep
        current_increment = 0
        actually_run = True
        while self.gossiping_run:
            if current_increment >= number_of_sleep_to_run:
                actually_run = True
            if actually_run:
                actually_run = False
                current_increment = 0
                self.gossiping_connect(read_callback)
            time.sleep(gossip_sleep)
            current_increment += 1

    def start_gossiping(self, read_callback):
        """
        Method to start gossiping threads to talk to peers and get their known peers

        Arguments:
        read_callback -- callback to which redirect msg from newly connected peers
        """
        if not self.gossiping_run:
            self.gossiping_run = True
            a_thread = threading.Thread(target=self.gossiping_listen)
            a_thread.start()
            b_thread = threading.Thread(target=self.gossiping_connect_thread, args=(read_callback,))
            b_thread.start()
            self.gossip_threads.append(a_thread)
            self.gossip_threads.append(b_thread)

    def join_network(self, bootstrap_host, peer_timeout=10, recv_data_size=1024, \
            socket_timeout=10, read_callback=None, wallet_callback=None, \
            start_bootstrap=False, start_gossiping=False):
        """
        Join the network and start communications

        Arguments:
        bootstrap_host -- host name of the bootstrap node. Can be itself
        peer_timeout=10 -- timeout on the peer before it is considered to be inactive
        recv_data_size=1024 -- default read size
        socket_timeout=10 -- timeout on socket recv
        read_callback=None -- callback to which redirect recv msgs
        wallet_callback=None -- callback to which redirect wallet connection
        start_bootstrap=False -- do we need to start a bootstrap node
        start_gossiping=False -- do we need to start gossiping threads
        """
        if read_callback is None:
            callback = Node.read_callback
        else:
            callback = read_callback
        if not self.bootstrap_node_running and start_bootstrap:
            self.start_bootstrap()
            # connect to its own bootstrap so it has information about itself
            self.connect_to_bootstrap(host=self.get_my_host(), port=self.default_bootstrap_port)
        known_peers = self.connect_to_bootstrap(host=bootstrap_host, port=self.default_bootstrap_port)
        self.connection_manager = connection_manager.ConnectionManager(server_port=self.port, \
                peer_timeout=peer_timeout, recv_data_size=recv_data_size, socket_timeout=socket_timeout)
        self.connection_manager.accept_connection(read_callback=callback, run_as_a_thread=True, wallet_callback=wallet_callback)
        first_peer = True
        for peer in known_peers:
            connected = self.peer_connection(peer, read_callback=read_callback)
            if first_peer and connected:
                first_peer = False
                self.doing_blockchain_sync = True
                self.send_sync_request(peer)
        if start_gossiping:
            self.start_gossiping(callback)

    def peer_connection(self, peer, read_callback=None):
        """
        Communication with a regular node during connection

        Arguments:
        peer -- peer to connect to
        read_callback=None -- callback to which redirect recv msgs
        Returns:
        bool -- was the connection successful
        """
        if read_callback is None:
            callback = Node.read_callback
        else:
            callback = read_callback
        if self.host == peer.ip_address and self.port == int(peer.port):
            return False
        return self.connection_manager.connect_to(host=peer.ip_address, \
                port=int(peer.port), read_callback=callback)

    def send_sync_request(self, peer):
        """
        Send a sync request to a peer

        Arguments:
        peer -- peer to send send request to
        """
        if self._do_block_sync:
            my_current_height = block_service.BlockService.get_max_height()
            message_obj = message.Message(action='init_sync', data=my_current_height)
            json_dic = message_obj.to_json(is_object=False)
            json_str = json.dumps(json_dic, sort_keys=True, separators=(',', ':'))
            id_to_send = ''
            # because id in peer that is received from a bootstrap node
            # is different from id that is was assigned when we connected to it
            # we need to find that id
            for a_peer in self.connection_manager.peer_list:
                if a_peer.get_ip_address() == peer.get_ip_address():
                    id_to_send = a_peer.peer_id
                    break
            self.connection_manager.send_msg(json_str, id_to_send)

    def add_blocks_from_queue(self):
        """
        After the sync is done we should add blocks that are in the queue
        """
        block_service_obj = block_service.BlockService()
        for a_block in self.block_queue:
            block_service_obj.add_block_to_chain(a_block)
        self.block_queue = []

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
        host = self.get_my_host()
        self.host = host
        client.send_msg(str(host) + ':' + str(self.port))
        recv_data = client.recv_msg(decode=False)
        known_peers = pickle.loads(recv_data)
        client.close_socket()
        return known_peers

    def get_my_host(self):
        return socket.gethostbyname(socket.getfqdn())

    def close(self):
        """
        Clean up and end node
        """
        if self.gossiping_run:
            self.gossiping_run = False
            self.unblock_gossiping_listen()
            for a_thread in self.gossip_threads:
                a_thread.join()
        self.connection_manager.close_all()
        if self.bootstrap_node_running:
            self.bootstrap_node.close()
