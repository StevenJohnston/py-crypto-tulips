from dal.objects import block, transaction
from dal.services import block_service, hash_service

block.Block.block_hash = "testing"

b = block.Block("hash_of_matt", "matt")

service = block_service.BlockService()

stored = service.store_block(b)
print("stored: " + str(stored))

new_block = service.find_by_hash(b.block_hash)
print("newblock: " + str(new_block.to_string()))

#print("dir of block->" + str(dir(b)))

t = transaction.Transaction("asdf", "to", "from", 6.54, "today")

#print("dir of transaction->" + str(dir(t)))

hs = hash_service.HashService()
hs.store_hash(t)

asdf = hs.get_object_by_hash(t.transaction_hash, transaction.Transaction)
new_t = transaction.Transaction.from_dict(asdf)

print(new_t.to_string())