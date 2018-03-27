from crypto_tulips.p2p.p2p_client import P2pClient
from crypto_tulips.p2p import message
from crypto_tulips.hashing.crypt_hashing_wif import EcdsaHashing
import json
from crypto_tulips.dal.objects.transaction import Transaction
import time

from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.services.contract_service import ContractService, ContractFilter

william_private_key = """55a1281dfe6cf404816be8f2bb33813e2cf8ef499fb22e21cb090f8f8563a72a"""

temp_key = """83c82312b925e50dde81f57f88f2fe1fb8310de1d81e97b696235c6093cd6af8"""

nk = "418a3147a90f519cd72fb05eb2f201368ee7265f36efb8824e9daed59aabe9e0"
denys_private_key = """f5dd743c84ddec77330b5dcf7e1f69a26ec55e0aa4fe504307b83f7850782510"""

if __name__ == '__main__':
    p2p = P2pClient(silent = False)
    p2p.connect_to('vagrant', 36363)
    p2p.send_msg('wallet')
    #Start getting balance, trans history and pending trans
    denys_public_key = EcdsaHashing.recover_public_key_str(denys_private_key)
    william_public_key = EcdsaHashing.recover_public_key_str(temp_key)
    nkey = EcdsaHashing.recover_public_key_str(nk)
    print(nkey)
    #william_public_key = '4dc0891733e18601025d2509ea2008661a916078af92237cf4e624ed9aed4419'
    # transaction_msg = message.Message('get_user_info', william_public_key)
    # transaction_json = transaction_msg.to_json(is_object=False)
    # transaction_json = json.dumps(transaction_json, sort_keys=True)
    # p2p.send_msg(transaction_json)
    # data = p2p.recv_msg()
    # print(data)
    #ends

    #Testing user wallet key generation
    #public_key = Hashing.get_public_key(temp)
    # print(public_key)
    # sig = Hashing.str_signature_of_data('message', temp)
    # print(sig)
    #ends user wallet testing

    #start a transaction
    # amount = 100
    # new_transaction = Transaction('', '', denys_public_key, william_public_key, amount, 1)
    # new_transaction.update_signature(william_private_key)
    # new_transaction.update_hash()

    # transaction_msg = message.Message('tx', new_transaction)
    # transaction_json = transaction_msg.to_json()
    # transaction_json = json.dumps(transaction_json, sort_keys=True)
    # print(transaction_json)
    # p2p.send_msg(transaction_json)
    # data = p2p.recv_msg()

    # msg = message.Message('get_all_ip', '')
    # msg_json = msg.to_json(is_object=False)
    # msg_json = json.dumps(msg_json, sort_keys=True)
    # p2p.send_msg(msg_json)


    contract_test = {"action": "get_contracts", "data": {
            "contractFilters": [
                {
                    "type": "contracts:rate",
                    "startRange": .4,
                    "endRange": .5
                },
                {
                    "type": "contracts:amount",
                    "startRange": 50,
                    "endRange": 1000
                }
            ]
        }
    }
    now = int(time.time())

    contractCreation = {"action": "publish_contract", "data": {
            "_hash": "tcs_hash1",
            "signature": "",
            "owner": william_public_key,
            "amount": "100",
            "rate": ".5",
            "is_mempool": 1,
            "duration": "1",
            "created_timestamp": 1521920465,
            "sign_end_timestamp": 1521920465
        }
    }
    scontract_test = {"action": "get_signed_contract", "data": {
            "contractFilters": [
                {
                    "type": "signed_contracts:amount",
                    "startRange": 50,
                    "endRange": 1000
                }
            ]
        }
    }

    get_user_contracts = {"action": "get_bitcoin_price", "data": {
            "userPublicKey": 'f80bb93e5ceb2de5c44d97b8a8f1a7f9778822292acb7642b9b14cab29b7476489c8cd0bff49490332eef64f859a7af2c89fd59dd6262011e2e2e3fb0e42808e'
        }
    }


    c = {'created_timestamp': 1521920465, 'amount': '100.00000000', 'sign_end_timestamp': 1521920465, 'rate': '0.50000000', 'owner': '2c1b95aa7ab8d18a6dda267a413117027cd05a26e5226fa01552d794d9ec87f13e0dbec0959e09ea5ab5665a9d81d25ee0f7d5c7145008d3e52cd60e6d204271', 'duration': 1}

    # contract_signable_json_str = json.dumps(c, sort_keys=True, separators=(',', ':'))
    # print(contract_signable_json_str)
    # sig = EcdsaHashing.sign_message_hex(contract_signable_json_str, temp_key)
    # print(sig)
    # transaction_json = json.dumps(contract_test, sort_keys=True)
   # p2p.send_msg(transaction_json)

    contract_json = json.dumps(get_user_contracts, sort_keys=True)
    p2p.send_msg(contract_json)
    # data = p2p.recv_msg()
    #print(data)
    #quiting
    transaction_msg = message.Message('exit', 'quit')
    transaction_json = transaction_msg.to_json(is_object=False)
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    p2p.send_msg(transaction_json)
    p2p.close_socket()
    #end
