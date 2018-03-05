import pytest
import json
import time
from crypto_tulips.dal.objects.pos_transaction import PosTransaction

##### Hashable tests #####

def test_hashable():
    test_time = int(time.time())
    pos_transaction = PosTransaction('pos_transaction_hash_test', '', 'steven_addr_test', 100, 0, test_time)
    actual = pos_transaction.get_hashable()
    expected = {
        'signature': '',
        'from_addr': 'steven_addr_test',
        'amount': 100,
        'timestamp': test_time
    }
    assert actual == expected

def test_hashable_fail():
    test_time = int(time.time())
    pos_transaction = PosTransaction('pos_transaction_hash_test', '', 'steven_addr_test', 100, 0, test_time)
    actual = pos_transaction.get_hashable()
    not_expected = {
        'signature': '',
        'from_addr': 'steven_addr_test_fail',
        'amount': 100,
        'timestamp': test_time
    }
    assert actual != not_expected

##### Sendable tests #####

def test_sendable():
    test_time = int(time.time())
    pos_transaction = PosTransaction('pos_transaction_hash_test', '', 'steven_addr_test', 100, 0, test_time)
    actual = pos_transaction.get_sendable()
    expected = {
        'signature': '',
        'from_addr': 'steven_addr_test',
        'amount': 100,
        'timestamp': test_time,
        '_hash': 'pos_transaction_hash_test'
    }
    assert actual == expected

def test_sendable_fail():
    test_time = int(time.time())
    pos_transaction = PosTransaction('pos_transaction_hash_test', '', 'steven_addr_test', 100, 0, test_time)
    actual = pos_transaction.get_hashable()
    not_expected = {
        'signature': '',
        'from_addr': 'steven_addr_test_fail',
        'amount': 100,
        'timestamp': test_time,
        '_hash': 'pos_transaction_hash_test_fail'
    }
    assert actual != not_expected