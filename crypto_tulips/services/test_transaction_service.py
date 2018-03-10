import pytest

from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.objects.transaction import Transaction

# create some transactions
transactions = [
    Transaction('ts_test_hash1', '', 'ts_matt', 'ts_william', 7000, 0),
    Transaction('ts_test_hash2', '', 'ts_steven', 'ts_william', 7000, 0),
    Transaction('ts_test_hash3', '', 'ts_steven', 'ts_william', 605, 0),
    Transaction('ts_test_hash4', '', 'ts_william', 'ts_naween', 14605, 0),

    Transaction('ts_test_hash5', '', 'ts_william', 'ts_naween', 14605, 1),
    Transaction('ts_test_hash6', '', 'ts_william', 'ts_naween', 14605, 1),
    Transaction('ts_test_hash7', '', 'ts_william', 'ts_naween', 14605, 1),
    Transaction('ts_test_hash8', '', 'ts_william', 'ts_naween', 14605, 1),
    Transaction('ts_test_hash9', '', 'ts_william', 'ts_naween', 14605, 1),
    Transaction('ts_test_hash10', '', 'ts_william', 'ts_naween', 14605, 1),
    Transaction('ts_test_hash11', '', 'ts_william', 'ts_naween', 14605, 1)
]

@pytest.mark.first
def setup():
    # run first to store test data in the database
    rs = RedisService()
    # store them
    for transaction in transactions:
        rs.store_object(transaction)

def test_get_transactions_by_public_key():
    ts = TransactionService()

    matt_t, matt_balance = ts.get_transactions_by_public_key('ts_matt', False)
    assert len(matt_t) == 1
    assert matt_balance == 7000
    assert matt_t.__contains__(transactions[0])
    assert not matt_t.__contains__(transactions[1])
    assert not matt_t.__contains__(transactions[2])
    assert not matt_t.__contains__(transactions[3])

    will_t, will_balance = ts.get_transactions_by_public_key('ts_william', False)
    assert len(will_t) == 4
    assert will_balance == 0
    assert will_t.__contains__(transactions[0])
    assert will_t.__contains__(transactions[1])
    assert will_t.__contains__(transactions[2])
    assert will_t.__contains__(transactions[3])

    naween_t, naween_balance = ts.get_transactions_by_public_key('ts_naween', False)
    assert len(naween_t) == 1
    assert naween_balance == -14605
    assert not naween_t.__contains__(transactions[0])
    assert not naween_t.__contains__(transactions[1])
    assert not naween_t.__contains__(transactions[2])
    assert naween_t.__contains__(transactions[3])

    steven_t, steven_balance = ts.get_transactions_by_public_key('ts_steven', False)
    assert len(steven_t) == 2
    assert steven_balance == 7605
    assert not steven_t.__contains__(transactions[0])
    assert steven_t.__contains__(transactions[1])
    assert steven_t.__contains__(transactions[2])
    assert not steven_t.__contains__(transactions[3])

def test_get_transactions_to_public_key():
    ts = TransactionService()

    matt_t  = ts.get_transactions_to_public_key('ts_matt', False)
    assert len(matt_t) == 1
    assert matt_t.__contains__(transactions[0])
    assert not matt_t.__contains__(transactions[1])
    assert not matt_t.__contains__(transactions[2])
    assert not matt_t.__contains__(transactions[3])

    naween_t  = ts.get_transactions_to_public_key('ts_naween', False)
    assert len(naween_t) == 0

def test_get_transactions_from_public_key():
    ts = TransactionService()

    naween_t  = ts.get_transactions_from_public_key('ts_naween', False)
    assert len(naween_t) == 1
    assert not naween_t.__contains__(transactions[0])
    assert not naween_t.__contains__(transactions[1])
    assert not naween_t.__contains__(transactions[2])
    assert naween_t.__contains__(transactions[3])

    matt_t  = ts.get_transactions_from_public_key('ts_matt', False)
    assert len(matt_t) == 0


def test_remove_from_mempool():
    ts = TransactionService()
    rs = RedisService()

    t = Transaction('mem_test_hash4', '', 'mem_william', 'mem_naween', 14605, 1)
    rs.store_object(t)

    ts.remove_from_mem_pool(t)

    new_t = rs.get_object_by_hash('mem_test_hash4', Transaction)

    print(t.to_string())
    print(new_t.to_string())
    assert new_t.is_mempool == 0

