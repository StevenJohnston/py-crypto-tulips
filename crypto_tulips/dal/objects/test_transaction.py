import pytest
from crypto_tulips.dal.objects.transaction import Transaction
import json
import time

def test_hashable():
    test_time = time.time()
    transaction = Transaction('block_hash_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    actual = transaction.hashable()
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
    actual = transaction.hashable()
    not_expected = {
        'to_addr': 'to_steven_test',
        'from_addr': 'from_matt_test',
        'amount': 2,
        'timestamp': test_time
    }
    assert actual != not_expected