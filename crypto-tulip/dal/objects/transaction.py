# Stored in database as a hash with key:
#       transaction:hash

class Transaction:

    prefix = "transaction"

    transaction_hash = ''
    to_addr = ''
    from_addr = ''
    amount = ''
    timestamp = ''

    def __init__(self, transaction_hash, to_addr, from_addr, amount, timestamp):
        self.transaction_hash = transaction_hash
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.amount = amount
        self.timestamp = timestamp


    def _from_json(self, json_str):
        self.transaction_hash = ""