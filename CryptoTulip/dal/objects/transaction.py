# Stored in database with keys:
#       transaction:id:hash 
#       transaction:id:to-addr
#       transaction:id:from-addr
#       transaction:id:amount
#       transaction:id:timestamp

class Transaction:

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