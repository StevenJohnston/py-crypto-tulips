import pytest
import time

from crypto_tulips.services.block_service import BlockService

from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.dal.objects.terminated_contract import TerminatedContract
from crypto_tulips.dal.objects.signed_contract import SignedContract
from crypto_tulips.dal.objects.contract import Contract

now = time.time()

ct1 = ContractTransaction('hash1', 'sig1', 'matt', 'sc_will_to_steven', 'BTC', 'TPS', 100, 0, now + 5)
ct1.price = 7000

ct2 = ContractTransaction('hash2', 'sig2', 'matt', 'sc_will_to_steven', 'BTC', 'TPS', 100, 0, now)
ct2.price = 6000

ct3 = ContractTransaction('hash3', 'sig3', 'matt', 'sc_will_to_steven', 'TPS', 'BTC', 200, 0, now + 11)
ct3.price = 9000

ct4 = ContractTransaction('hash4', 'sig4', 'matt', 'sc_matt_to_naween', 'BTC', 'TPS', 100, 0, now+2)
ct4.price = 7000

ct5 = ContractTransaction('hash5', 'sig5', 'matt', 'sc_matt_to_naween', 'BTC', 'TPS', 100, 0, now+1)
ct5.price = 7000

ct6 = ContractTransaction('hash6', 'sig6', 'matt', 'sc_norb_to_denys', 'BTC', 'TPS', 100, 0, now)
ct6.price = 7000

ct7 = ContractTransaction('hash7', 'sig7', 'matt', 'sc_norb_to_denys', 'BTC', 'TPS', 40, 0, now)
ct7.price = 7000

tc1 = TerminatedContract('sc_matt_to_naween', 10000, now + 2)
tc2 = TerminatedContract('sc_norb_to_denys', 4000, now + 1)

c1 = Contract('con_steven', 'con_steven_sig', 'steven', 200, 0.4, 0, 1000, now - 100, now + 100)
c2 = Contract('con_naween', 'con_naween_sig', 'naween', 3000, 0.3, 0, 2000, now - 120, now + 1340)
c3 = Contract('con_denys', 'con_denys_sig', 'denys', 150, 0.34, 0, 1500, now - 130, now + 2033)

sc1 = SignedContract('sc_will_to_steven', 'sc_sig1', 'william', now + 10, 'con_steven', 'con_steven_sig', 'steven', 200, 0.4, 0, 100, now - 100, now)
sc2 = SignedContract('sc_matt_to_naween', 'sc_sig2', 'matt', now + 10, 'con_naween', 'con_naween_sig', 'naween', 3000, 0.3, 0, 2000, now - 120, now + 1340)
sc3 = SignedContract('sc_norb_to_denys', 'sc_sig3', 'norbert', now + 10, 'con_denys', 'con_denys_sig', 'denys', 150, 0.34, 0, 1500, now - 130, now + 2033)


owners = ['matt', 'steven', 'denys', 'william', 'norbert']
def test_get_all_balances():
    con_trans = [ct1, ct2, ct3, ct4, ct5, ct6, ct7]
    term_cs = [tc1, tc2]
    signed_cs = [sc1, sc2, sc3]
    cons = [c1, c2, c3]

    contract_transaction_dict = {contract_transaction._hash: contract_transaction for contract_transaction in con_trans}
    tcontract_dict = {terminated_contract._hash: terminated_contract for terminated_contract in term_cs}
    signed_dict = {signed_contract._hash: signed_contract for signed_contract in signed_cs}
    contract_dict = {contract._hash: contract for contract in cons}

    objects = {'contract_transactions': contract_transaction_dict, 'terminated_contracts': tcontract_dict, 'signed_contracts': signed_dict, 'contracts': contract_dict, 'owners': owners}
    balances = BlockService.get_all_balances(objects)
    print(balances)
    assert False
