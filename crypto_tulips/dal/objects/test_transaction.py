import pytest
from crypto_tulips.dal.objects.transaction import Transaction
import json
import time

##### Hashable Tests #####

def test_hashable():
    test_time = int(time.time())
    transaction = Transaction('block_hash_test', '', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_hashable()
    expected = {
        'signature': '',
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 1,
        'timestamp': test_time
    }
    assert actual == expected

def test_hashable_fail():
    test_time = int(time.time())
    transaction = Transaction('block_hash_test', '', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_hashable()
    not_expected = {
        'signature': '',
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 2,
        'timestamp': test_time
    }
    assert actual != not_expected

##### Sendable Tests #####

def test_sendable():
    test_time = int(time.time())
    transaction = Transaction('block_send_test', '', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_sendable()
    expected = {
        'signature': '',
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 1,
        'timestamp': test_time,
        '_hash': 'block_send_test'
    }
    assert actual == expected

def test_sendable_fail():
    test_time = int(time.time())
    transaction = Transaction('block_send_test', '', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_sendable()
    not_expected = {
        'signature': '',
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 2,
        'timestamp': test_time,
        '_hash': 'block_send_test'
    }
    assert actual != not_expected

def test_sendable_json():
    test_time = int(time.time())
    transaction = Transaction('block_send_test', '', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = json.dumps(transaction.get_sendable(), sort_keys=True)
    expected = json.dumps({
        'signature': '',
        'amount': 1.0,
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        '_hash': 'block_send_test',
        'timestamp': test_time
    }, sort_keys=True)
    assert actual == expected
    