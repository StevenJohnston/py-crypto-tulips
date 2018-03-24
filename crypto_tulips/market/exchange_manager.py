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
        
if __name__ == "__main__":
    ExchangeManager()