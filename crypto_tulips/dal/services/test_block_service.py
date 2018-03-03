import pytest

from crypto_tulips.dal.services.block_service import BlockService
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.dal.objects.transaction import Transaction

def test_get_store_block():
    t1 = Transaction('transaction_test_1', 'matt', 'will', 45)
    t2 = Transaction('transaction_test_2', 'matt', 'denys', 7)
    t3 = Transaction('transaction_test_3', 'denys', 'steven', 33)
    t4 = Transaction('transaction_test_4', 'steven', 'naween', 5040)
    t5 = Transaction('transaction_test_5', 'will', 'naween', 22)
    t6 = Transaction('transaction_test_6', 'naween', 'matt', 588)
    b = Block('block_service_test_1', [t1, t2, t3, t4, t5, t6], [], [])
    bs = BlockService()

    bs.store_block(b)

    new_b = bs.find_by_hash('block_service_test_1')

    assert b.get_sendable() == new_b.get_sendable()

def test_store_same_hash():
    b = Block('block_service_test_1', [], [], [])

    bs = BlockService()

    bs.store_block(b)

    new_b = bs.find_by_hash('block_service_test_1')

    assert b.get_sendable() != new_b.get_sendable()