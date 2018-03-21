"""
Module that containts class that combines functionality of p2p_server and p2p_client
"""

import threading
import socket
import time
from . import p2p_client
from . import p2p_server
from . import p2p_peer

class MarketManager:
    """
    Class that combines functionality of p2p_server and p2p_client.
    Class manages different client connections, different server connections.
    Additionally, class automatically communicates with different peers to determine which ones are
    still active and remove inactive.
    """

    def __init__(self, server_port=None, peer_timeout=10, recv_data_size=1024, socket_timeout=10):
        """
        Constructor

        Arguments:
        server_port=None -- on which port run server part of the ConnectionManager
        peer_timeout=10 -- time in seconds after which inactive peers will be removed
        recv_data_size=1024 -- read buffer size
        socket_timeout=10 -- time in seconds after which a socket read will timeout
        """
        self.server_port = None
        self.server = None
        self.peer_timeout = None
        self.recv_data_size = None
        self.run = True
        self.blocking_accept = False
        self.removing_peers = True
        self.peer_list = []
        self.runnings_threads = []
        self.socket_timeout = 10
        self.ok_response = '\x03'
        self.client_connection_msg = '\x01'

        self.socket_timeout = socket_timeout
        self.server_port = server_port
        self.peer_timeout = peer_timeout
        self.recv_data_size = recv_data_size
        self.server = p2p_server.P2pServer(server_port, data_size=recv_data_size)
        if peer_timeout > 0:
            a_thread = threading.Thread(target=self.auto_remove_peers, args=())
            self.runnings_threads.append(a_thread)
            a_thread.start()

    def __del__(self):
        if not self.peer_list:
            print('Peer list is empty')
        else:
            print('Peer list has {} peers, two can exist from unblocking'.format(len(self.peer_list)))
        for a_thread in self.runnings_threads:
            a_thread.join()
        print('All threads are joined')

    def connect_to(self, host, port, read_callback):
        """
        Connect to a provided server

        Arguments:
        host -- host to connect to
        port -- port to connect to
        read_callback -- a callback function that is going to be called when msg is received. Requires data argument
        """
        client = p2p_client.P2pClient(data_size=self.recv_data_size)
        client.connect_to(host, port)
        client.send_msg(self.client_connection_msg)
        response = client.recv_msg()
        if response != self.ok_response:
            pass
        client.set_timeout(self.socket_timeout)
        peer = p2p_peer.Peer(socket=client, ip_address=host, port=port, mode=p2p_peer.PeerMode.Client)
        peer.make_timestamp()
        self.peer_list.append(peer)
        self.start_recv_thread(peer=peer, callback=read_callback, target=self.recv_msg_client)
        print('Client connected to a server and started to recv')

    def start_recv_thread(self, peer, callback, target):
        """
        Method to stat a new thread to recv msgs

        Arguments:
        peer -- peer that is going to recv msgs
        callback -- callback to call when msg is received
        target -- method to execute in a thread
        """
        a_thread = threading.Thread(target=target, args=(peer, callback))
        self.runnings_threads.append(a_thread)
        a_thread.start()

    def accept_connection(self, read_callback, run_as_a_thread=False):
        """
        Accept client connection

        Arguments:
        read_callback -- a callback function that is going to be called when msg is received. Requires data argument
        run_as_a_thread=False -- accept clients until server is closed in a thread
        """
        if not run_as_a_thread:
            self.accept_connection_one(read_callback)
        else:
            a_thread = threading.Thread(target=self.accept_connection_threading, args=(read_callback,))
            self.runnings_threads.append(a_thread)
            a_thread.start()
            self.blocking_accept = True

    def accept_connection_one(self, read_callback):
        """
        Method to accept one client connection

        Arguments:
        read_callback -- callback to call when msg is received
        """
        client_pair = self.server.accept_client()
        response = self.server.recv_msg(client_pair=client_pair)
        if response != self.client_connection_msg:
            pass
        self.server.send_msg(self.ok_response, client_pair=client_pair)
        self.server.set_timeout(self.socket_timeout, client_pair=client_pair)
        peer = p2p_peer.Peer(socket=client_pair.socket, ip_address=client_pair.address, mode=p2p_peer.PeerMode.Server)
        peer.make_timestamp()
        self.peer_list.append(peer)
        self.start_recv_thread(peer=peer, callback=read_callback, target=self.recv_msg_server)
        print('Server got a connection and started to recv')

    def accept_connection_threading(self, read_callback):
        """
        Method to run as a thread and accept clients until server is stopped

        Arguments:
        read_callback -- callback to call when msg is received
        """
        while self.run:
            self.accept_connection_one(read_callback)

    def auto_remove_peers(self):
        """
        Method to run in a thread and remove peers automatically
        """
        while self.removing_peers:
            time_to_sleep = self.remove_peers()
            time.sleep(time_to_sleep)
        print('Stopped auto removing peers')

    def remove_peers(self):
        """
        Method to remove peers that have not send any msges for some time
        """
        time_to_sleep = self.peer_timeout
        smallest_time_difference = float("inf")
        peers_to_remove = []
        for peer in self.peer_list:
            difference = int(peer.give_time_difference())
            if difference < smallest_time_difference:
                smallest_time_difference = difference
            if difference >= self.peer_timeout:
                peers_to_remove.append(peer)
        if smallest_time_difference < self.peer_timeout and smallest_time_difference >= 0:
            time_to_sleep = self.peer_timeout - smallest_time_difference
        print("Removing {} peers out of {}".format(len(peers_to_remove), len(self.peer_list)))
        print("Want to sleep for {}".format(time_to_sleep))
        while peers_to_remove:
            try:
                self.close_peer(peers_to_remove.pop(0))
            except ValueError as ex:
                print('peer was already removed, {}'.format(ex))
        return time_to_sleep

    def unblock_accept(self):
        """
        Method to unblock blocking accept clients
        """
        client = p2p_client.P2pClient(data_size=self.recv_data_size)
        host = socket.gethostname()
        client.connect_to(host, self.server_port)
        client.send_msg(self.client_connection_msg)
        response = client.recv_msg()
        if response != self.ok_response:
            pass
        peer = p2p_peer.Peer(socket=client, ip_address=host, port=None, mode=p2p_peer.PeerMode.Client)
        self.peer_list.append(peer)
        print('Unblocking client connected to its own server')

    def send_msg_client(self, msg, peer):
        """
        Send a msg to a given peer, using a client

        Argumetns:
        msg -- msg to send
        peer -- peer to whom send a msg
        """
        peer_client = peer.socket
        peer_client.send_msg(msg)

    def send_msg_server(self, msg, peer):
        """
        Semd a ,sg tp a govem peer, using a server

        Arguments:
        msg -- msg to send
        peer -- peer to whom send a msg
        """
        self.server.send_msg(msg, client_socket=peer.socket)

    def send_msg(self, msg):
        """
        Send a data message to all peers in a peer list

        Arguments:
        msg -- a msg to send to all connected peers
        """
        for peer in self.peer_list:
            if peer.mode == p2p_peer.PeerMode.Client:
                self.send_msg_client(msg, peer)
            elif peer.mode == p2p_peer.PeerMode.Server:
                self.send_msg_server(msg, peer)

    def recv_msg_client(self, peer, callback):
        """
        Method to read msgs from a peer and forward them to a given callback

        Arguments:
        peer -- peer client to recv msg
        callback -- function to be called when data is received. Requires data argument
        """
        while self.run:
            try:
                recv_data = peer.socket.recv_msg()
            except socket.timeout:
                print('Socket timeout on a client read')
            except OSError as ex:
                if ex.errno == 9:
                    print("Other side's socket on client read got closed")
                else:
                    print('Unknown client OSError, {}'.format(ex))
                break
            else:
                if recv_data != '':
                    peer.make_timestamp()
                    callback(data=recv_data)#"""
        print('Ended a recv msg client thread, run is {}'.format(self.run))

    def recv_msg_server(self, peer, callback):
        """
        Them to read msgs from a peer and forward them to a given callback

        Arguments:
        peer -- peer server to recv msg
        callback -- function to be called when data is received. Requires data argument
        """
        while self.run:
            try:
                recv_data = self.server.recv_msg(client_socket=peer.socket)
            except socket.timeout:
                print('Socket timeout on server read')
            except OSError as ex:
                if ex.errno == 9:
                    print("Other side's socket on server read got closed")
                else:
                    print('Unknown server OSError, {}'.format(ex))
                break
            else:
                if recv_data != '':
                    peer.make_timestamp()
                    callback(data=recv_data)
        print('Ended a recv msg server thread, run is {}'.format(self.run))

    def close_peer(self, peer, remove_peer=True):
        """
        Close one peer and remove it from the list

        Arguments:
        peer -- peer to close
        remove_peer=True -- remove peer from the list of all peers
        """
        if peer.mode == p2p_peer.PeerMode.Client:
            peer.socket.close_socket()
        elif peer.mode == p2p_peer.PeerMode.Server:
            self.server.close_client(client_socket=peer.socket)
        if remove_peer:
            self.peer_list.remove(peer)

    def close_all(self):
        """
        Cleanup to close all connection
        """
        self.run = False
        self.removing_peers = False
        if self.blocking_accept:
            self.unblock_accept()
            self.blocking_accept = False
        for peer in self.peer_list:
            self.close_peer(peer, remove_peer=False)
        self.server.close_socket()
        for a_thread in self.runnings_threads:
            a_thread.join()
