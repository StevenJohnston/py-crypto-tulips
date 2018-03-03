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


##### Hashable tests #####

def test_hashable():
    curr_time = time.time()
    block = Block('block_hash_test', [], [], [], curr_time)
    actual = block.get_hashable()
    expected = {
        'transactions': [],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': curr_time
    }
    assert actual == expected

def test_hashable_fail():
    curr_time = time.time()
    block = Block('block_hash_test', [], [], [], curr_time)
    actual = block.get_hashable()
    not_expected = {
        'transactions': [],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': time.time()
    }
    assert actual != not_expected

def test_transaction_hashable_fail():
    test_time = time.time()
    block_time = time.time()
    transaction_1 = Transaction('block_hash_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    transaction_2 = Transaction('block_hash_test2', 'to_matt_test', 'from_steven_test', 1, test_time)
    block = Block('block_hash_test', [
        transaction_1,
        transaction_2
    ], [], [], block_time)
    actual = block.get_hashable()
    expected = {
        'transactions': [
            transaction_1.get_sendable(),
            transaction_2.get_sendable()
        ],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': block_time
    }
    assert actual == expected


##### Sendable tests #####

def test_sendable():
    curr_time = time.time()
    block = Block('block_send_test', [], [], [], curr_time)
    actual = block.get_sendable()
    expected = {
        'transactions': [],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': curr_time,
        'block_hash': 'block_send_test'
    }
    assert actual == expected

def test_sendable_fail():
    curr_time = time.time()
    block = Block('block_send_test', [], [], [], curr_time)
    actual = block.get_sendable()
    not_expected = {
        'transactions': [],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': 'time_here_tests',
        'block_hash': 'block_send_test'
    }
    assert actual != not_expected

def test_transaction_sendable_fail():
    test_time = time.time()
    block_time = time.time()
    transaction_1 = Transaction('block_send_test', 'to_steven_test', 'from_matt_test', 1, test_time)
    transaction_2 = Transaction('block_send_test2', 'to_matt_test', 'from_steven_test', 1, test_time)
    block = Block('block_send_test', [
        transaction_1,
        transaction_2
    ], [], [], block_time)
    actual = block.get_sendable()
    expected = {
        'transactions': [
            transaction_1.get_sendable(),
            transaction_2.get_sendable()
        ],
        'pos_transactions': [],
        'contract_transactions': [],
        'timestamp': block_time,
        'block_hash': 'block_send_test'
    }
    assert actual == expected