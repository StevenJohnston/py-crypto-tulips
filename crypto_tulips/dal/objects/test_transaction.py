import pytest
from crypto_tulips.dal.objects.transaction import Transaction
import json
import time

##### Hashable Tests #####

def test_hashable():
    test_time = time.time()
    transaction = Transaction('block_hash_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_hashable()
    expected = {
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 1,
        'timestamp': test_time
    }
    assert actual == expected

def test_hashable_fail():
    test_time = time.time()
    transaction = Transaction('block_hash_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_hashable()
    not_expected = {
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 2,
        'timestamp': test_time
    }
    assert actual != not_expected

##### Sendable Tests #####

def test_sendable():
    test_time = time.time()
    transaction = Transaction('block_send_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_sendable()
    expected = {
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 1,
        'timestamp': test_time,
        '_hash': 'block_send_test'
    }
    assert actual == expected

def test_sendable_fail():
    test_time = time.time()
    transaction = Transaction('block_send_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.get_sendable()
    not_expected = {
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 2,
        'timestamp': test_time,
        '_hash': 'block_send_test'
    }
    assert actual != not_expected
