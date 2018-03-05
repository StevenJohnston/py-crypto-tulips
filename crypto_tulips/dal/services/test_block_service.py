import pytest
import time

from crypto_tulips.dal.services.block_service import BlockService
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.dal.objects.transaction import Transaction

@pytest.mark.first
def test_get_store_block():
    test_time = int(time.time())
    t1 = Transaction('transaction_test_1', '', 'matt', 'will', 45, 0, test_time)
    t2 = Transaction('transaction_test_2', '', 'matt', 'denys', 7, 0, test_time)
    t3 = Transaction('transaction_test_3', '', 'denys', 'steven', 33, 0, test_time)
    t4 = Transaction('transaction_test_4', '', 'steven', 'naween', 5040, 0, test_time)
    t5 = Transaction('transaction_test_5', '', 'will', 'naween', 22, 0, test_time)
    t6 = Transaction('transaction_test_6', '', 'naween', 'matt', 588, 0, test_time)
    b = Block('block_service_test_1', '', '', 0, [t1, t2, t3, t4, t5, t6], [], [], test_time)
    bs = BlockService()

    bs.store_block(b)

    new_b = bs.find_by_hash('block_service_test_1')

    assert b.get_sendable() == new_b.get_sendable()

def test_store_same_hash():
    b = Block('block_service_test_1', '', '', 0, [], [], [])

    bs = BlockService()

    bs.store_block(b)

    new_b = bs.find_by_hash('block_service_test_1')

    assert b.get_sendable() != new_b.get_sendable()