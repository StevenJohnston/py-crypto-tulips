import json
import redis
from objects import transaction

class TransactionService:
    __host = ''
    __port = 3000

    key_format = 'transaction:{}'

    def __init__(self):
        settings = json.load(open('db_settings.json'))
        print(settings["host"] + ":" + settings["port"])
        self.host = settings["host"]
        self.port = settings["port"]

    def store_transaction(self, transaction):
        r = self.__connect()
        json_transaction = json.encoder(transaction)
        r.set(key_format.format(transaction.))

        return

    def find_by_hash(self, block_hash):
        r = self.__connect()

        block_data = r.get(block_hash)
        b = block.Block(block_hash, block_data)
        print("newblock=" + b.to_string())
        return b

    def __connect(self):
        return redis.Redis(self.host, self.port, db=0)
