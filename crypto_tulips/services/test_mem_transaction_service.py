import pytest

from crypto_tulips.services.mem_transaction_service import MemTransactionService
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.objects.mem_transaction import MemTransaction

# create some transactions
t1 = MemTransaction('mts_test_hash1', 'mts_matt', 'mts_william', 7000)
t2 = MemTransaction('mts_test_hash2', 'mts_steven', 'mts_william', 7000)
t3 = MemTransaction('mts_test_hash3', 'mts_steven', 'mts_william', 605)
t4 = MemTransaction('mts_test_hash4', 'mts_william', 'mts_naween', 14605)

@pytest.mark.first
def setup():
    # run first to store test data in the database
    rs = RedisService()
    # store them
    rs.store_object(t1)
    rs.store_object(t2)
    rs.store_object(t3)
    rs.store_object(t4)

def test_get_transactions_by_public_key():
    mts = MemTransactionService()

    matt_t, matt_balance = mts.get_transactions_by_public_key('mts_matt')
    assert len(matt_t) == 1
    assert matt_balance == 7000
    assert matt_t.__contains__(t1)
    assert not matt_t.__contains__(t2)
    assert not matt_t.__contains__(t3)
    assert not matt_t.__contains__(t4)

    will_t, will_balance = mts.get_transactions_by_public_key('mts_william')
    assert len(will_t) == 4
    assert will_balance == 0
    assert will_t.__contains__(t1)
    assert will_t.__contains__(t2)
    assert will_t.__contains__(t3)
    assert will_t.__contains__(t4)

    naween_t, naween_balance = mts.get_transactions_by_public_key('mts_naween')
    assert len(naween_t) == 1
    assert naween_balance == -14605
    assert not naween_t.__contains__(t1)
    assert not naween_t.__contains__(t2)
    assert not naween_t.__contains__(t3)
    assert naween_t.__contains__(t4)

    steven_t, steven_balance = mts.get_transactions_by_public_key('mts_steven')
    assert len(steven_t) == 2
    assert steven_balance == 7605
    assert not steven_t.__contains__(t1)
    assert steven_t.__contains__(t2)
    assert steven_t.__contains__(t3)
    assert not steven_t.__contains__(t4)

def test_get_transactions_to_public_key():
    mts = MemTransactionService()

    matt_t  = mts.get_transactions_to_public_key('mts_matt')
    assert len(matt_t) == 1
    assert matt_t.__contains__(t1)
    assert not matt_t.__contains__(t2)
    assert not matt_t.__contains__(t3)
    assert not matt_t.__contains__(t4)

    naween_t  = mts.get_transactions_to_public_key('mts_naween')
    assert len(naween_t) == 0

def test_get_transactions_from_public_key():
    mts = MemTransactionService()

    naween_t  = mts.get_transactions_from_public_key('mts_naween')
    assert len(naween_t) == 1
    assert not naween_t.__contains__(t1)
    assert not naween_t.__contains__(t2)
    assert not naween_t.__contains__(t3)
    assert naween_t.__contains__(t4)

    matt_t  = mts.get_transactions_from_public_key('mts_matt')
    assert len(matt_t) == 0