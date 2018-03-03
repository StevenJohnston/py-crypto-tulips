import pytest
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.dal.objects.transaction import Transaction
import json
import time

def map_func(val): 
    return val + 0
def test_map_test():
    my_list = [1,2,3,4]
    actual = list(map(map_func, my_list))
    expected = [1,2,3,4]
    assert actual == expected

def test_hashable():
    block = Block('block_hash_test', [], [], [], 'time_here_test')
    actual = block.hashable()
    expected = {
        'transactions': [],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': 'time_here_test'
    }
    assert actual == expected

def test_hashable_fail():
    block = Block('block_hash_test', [], [], [], 'time_here_test')
    actual = block.hashable()
    not_expected = {
        'transactions': [],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': 'time_here_tests'
    }
    assert actual != not_expected

def test_transaction_hashable_fail():
    test_time = time.time()
    transaction_1 = Transaction('block_hash_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    transaction_2 = Transaction('block_hash_test2', 'to_matt_test', 'from_steven_test', 1, test_time)
    block = Block('block_hash_test', [
        transaction_1, 
        transaction_2
    ], [], [], 'time_here_test')
    actual = block.hashable()
    expected = {
        'transactions': [
            transaction_1.hashable(),
            transaction_2.hashable()
        ],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': 'time_here_test'
    }
    assert actual == expected
