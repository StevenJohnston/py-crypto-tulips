from objects import block
from services import block_service

print("testing")
b = block.Block("hash of matt", "matt")
service = block_service.BlockService()

stored = service.store_block(b)
print("stored: " + str(stored))


new_block = service.find_by_hash(b.block_hash)
#print("newblock: " + str(new_block.to_string()))
