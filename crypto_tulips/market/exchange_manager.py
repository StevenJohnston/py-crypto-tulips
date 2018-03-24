import threading
import socket
import time
from .bitfinex import Bitfinex

class ExchangeManager:
    def __init__(self):
        self.exchanges = [
            Bitfinex()
        ]
        for exchange in self.exchanges:
            exchange.start()

    def __del__(self):
        print('Peer list is empty')
        
if __name__ == "__main__":
    ExchangeManager()