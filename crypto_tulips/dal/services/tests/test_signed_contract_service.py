import pytest
import redis
import time

from crypto_tulips.dal.services.signed_contract_service import SignedContractService, SignedContractFilter
from crypto_tulips.dal.objects.signed_contract import SignedContract

now = int(time.time())
c1 = SignedContract('tsignc_hash1', 'tsignc_sig1', 'tsignc_denys', now, 'tsignc_p_hash1', 'tsignc_p_sig1', 'tsignc_p_matt', 100, 0.5, 1, 1000, now, now + 900)
c2 = SignedContract('tsignc_hash2', 'tsignc_sig2', 'tsignc_naween', now, 'tsignc_p_hash2', 'tsignc_p_sig2', 'tsignc_p_matt', 50, 0.3, 1, 10000, (now + 1000), now + 9000)
c3 = SignedContract('tsignc_hash3', 'tsignc_sig3', 'tsignc_william', now, 'tsignc_p_hash3', 'tsignc_p_sig3', 'tsignc_p_denys', 1239, 0.7, 1, 100040, (now + 2000), now + 90040)
c4 = SignedContract('tsignc_hash4', 'tsignc_sig4', 'tsignc_steven', now, 'tsignc_p_hash4', 'tsignc_p_sig4', 'tsignc_p_naween', 10430, 0.1, 1, 13040, (now + 3000), now + 12040)
c5 = SignedContract('tsignc_hash5', 'tsignc_sig5', 'tsignc_denys', now + 1000, 'tsignc_p_hash5', 'tsignc_p_sig5', 'tsignc_p_william', 54, 0.4, 1, 15404, (now + 4000), now + 14404)

@pytest.mark.first
def setup():
    SignedContractService.store_signed_contract(c1)
    SignedContractService.store_signed_contract(c2)
    SignedContractService.store_signed_contract(c3)
    SignedContractService.store_signed_contract(c4)
    SignedContractService.store_signed_contract(c5)


def test_get_signed_contract_by_hash():
    signed_contract = SignedContractService.get_signed_contract_by_hash(c1._hash)
    assert c1.get_sendable() == signed_contract.get_sendable()

# FILTER TESTS

def test_get_signed_contracts_by_amount_range():
    cf = SignedContractFilter(SignedContractFilter.AMOUNT, 100, 1000)
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf], True)
    assert len(signed_contracts) == 1
    assert signed_contracts[0].get_sendable() == c1.get_sendable()
    cf.maximum = 10000
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf], True)
    assert len(signed_contracts) == 2

def test_get_signed_contracts_by_rate_range():
    cf = SignedContractFilter(SignedContractFilter.RATE, 0.5, 0.7)
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf], True)
    assert len(signed_contracts) == 2

def test_get_signed_contracts_by_signed_range():
    cf = SignedContractFilter(SignedContractFilter.SIGNED, now, now)
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf], True)
    assert len(signed_contracts) == 4

def test_get_signed_contracts_by_duration_range():
    cf = SignedContractFilter(SignedContractFilter.DURATION, 1000, 13040)
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf], True)
    assert len(signed_contracts) == 3

def test_get_signed_contracts_by_multiple():
    cf1 = SignedContractFilter(SignedContractFilter.AMOUNT, 50, 1000) # c2, c5, c1
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf1], True)
    assert len(signed_contracts) == 3

    cf2 = SignedContractFilter(SignedContractFilter.RATE, 0.4, 0.5) # c1, c5
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf1, cf2], True)
    assert len(signed_contracts) == 2

    cf3 = SignedContractFilter(SignedContractFilter.DURATION, 15404, 15404) # c5
    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf1, cf2, cf3], True)
    assert len(signed_contracts) == 1

    signed_contracts = SignedContractService.get_signed_contracts_by_filter([cf1, cf2, cf3], False) # None
    assert len(signed_contracts) == 0

# END OF FILTER TESTS


@pytest.mark.last
def end_closing():
    r = redis.Redis()
    r.flushdb()