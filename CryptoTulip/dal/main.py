from .block import block, block_service

def main():
    b = block.Block("hash of matt", "matt")
    service = block_service.BlockService()

    stored = service.store_block(b)
    print("stored: " + stored)


    new_block = service.find_by_hash(b.block_hash)
    print("newblock: " + new_block.to_string())
