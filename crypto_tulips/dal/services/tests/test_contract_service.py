import pytest
import redis
import time

from crypto_tulips.dal.services.contract_service import ContractService, ContractFilter
from crypto_tulips.dal.objects.contract import Contract

now = int(time.time())
c1 = Contract('tcs_hash1', 'tcs_sig1', 'tc_matt', 100, 0.5, 1, 1000, now, now + 900)
c2 = Contract('tcs_hash2', 'tcs_sig2', 'tc_matt', 50, 0.3, 1, 10000, (now + 1000), now + 9000)
c3 = Contract('tcs_hash3', 'tcs_sig3', 'tc_denys', 1239, 0.7, 1, 100040, (now + 2000), now + 90040)
c4 = Contract('tcs_hash4', 'tcs_sig4', 'tc_naween', 10430, 0.1, 1, 13040, (now + 3000), now + 12040)
c5 = Contract('tcs_hash5', 'tcs_sig5', 'tc_william', 54, 0.4, 1, 15404, (now + 4000), now + 14404)

@pytest.mark.first
def setup():
    ContractService.store_contract(c1)
    ContractService.store_contract(c2)
    ContractService.store_contract(c3)
    ContractService.store_contract(c4)
    ContractService.store_contract(c5)


def test_get_contract_by_hash():
    contract = ContractService.get_contract_by_hash(c1._hash)
    assert c1.get_sendable() == contract.get_sendable()

# FILTER TESTS

def test_get_contracts_by_amount_range():
    cf = ContractFilter(ContractFilter.AMOUNT, 100, 1000)
    contracts = ContractService.get_contracts_by_filter([cf], True)
    assert len(contracts) == 1
    assert contracts[0].get_sendable() == c1.get_sendable()
    cf.maximum = 10000
    contracts = ContractService.get_contracts_by_filter([cf], True)
    assert len(contracts) == 2

def test_get_contracts_by_rate_range():
    cf = ContractFilter(ContractFilter.RATE, 0.5, 0.7)
    contracts = ContractService.get_contracts_by_filter([cf], True)
    assert len(contracts) == 2

def test_get_contracts_by_created_range():
    cf = ContractFilter(ContractFilter.CREATED, now, now + 3000)
    contracts = ContractService.get_contracts_by_filter([cf], True)
    assert len(contracts) == 4

def test_get_contracts_by_duration_range():
    cf = ContractFilter(ContractFilter.DURATION, 1000, 13040)
    contracts = ContractService.get_contracts_by_filter([cf], True)
    assert len(contracts) == 3

def test_get_contracts_by_multiple():
    cf1 = ContractFilter(ContractFilter.AMOUNT, 50, 1000) # c2, c5, c1
    contracts = ContractService.get_contracts_by_filter([cf1], True)
    assert len(contracts) == 3

    cf2 = ContractFilter(ContractFilter.RATE, 0.4, 0.5) # c1, c5
    contracts = ContractService.get_contracts_by_filter([cf1, cf2], True)
    assert len(contracts) == 2

    cf3 = ContractFilter(ContractFilter.DURATION, 15404, 15404) # c5
    contracts = ContractService.get_contracts_by_filter([cf1, cf2, cf3], True)
    assert len(contracts) == 1

    contracts = ContractService.get_contracts_by_filter([cf1, cf2, cf3], False) # None
    assert len(contracts) == 0

# END OF FILTER TESTS

def test_get_all_contracts_by_owner():
    contracts = ContractService.get_all_contracts_by_owner('tc_matt')
    assert len(contracts) == 2
    for contract in contracts:
        assert contract.owner == 'tc_matt'

    contracts = ContractService.get_all_contracts_by_owner('tc_denys')
    assert len(contracts) == 1
    for contract in contracts:
        assert contract.owner == 'tc_denys'

    contracts = ContractService.get_all_contracts_by_owner('bad_key')
    assert len(contracts) == 0

@pytest.mark.last
def end_closing():
    r = redis.Redis()
    r.flushdb()