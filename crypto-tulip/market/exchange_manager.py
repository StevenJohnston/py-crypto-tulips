"""
Module that containts class that combines functionality of p2p_server and p2p_client
"""

import threading
import socket
import time
from . import bitfinex

class ExchangeManager:
    """
    Class that combines functionality of p2p_server and p2p_client.
    Class manages different client connections, different server connections.
    Additionally, class automatically communicates with different peers to determine which ones are
    still active and remove inactive.
    """

    def __init__(self):
        self.exchanges = [
            bitfinex
        ]

    def __del__(self):
        if not self.peer_list:
            print('Peer list is empty')
        else:
            print('Peer list has {} peers, two can exist from unblocking'.format(len(self.peer_list)))
        for a_thread in self.runnings_threads:
            a_thread.join()
        print('All threads are joined')