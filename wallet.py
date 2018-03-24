from crypto_tulips.p2p.p2p_client import P2pClient
from crypto_tulips.p2p import message
from crypto_tulips.hashing.crypt_hashing_wif import EcdsaHashing
import json
from crypto_tulips.dal.objects.transaction import Transaction

william_private_key = """55a1281dfe6cf404816be8f2bb33813e2cf8ef499fb22e21cb090f8f8563a72a"""

temp_key = """83c82312b925e50dde81f57f88f2fe1fb8310de1d81e97b696235c6093cd6af8"""


denys_private_key = """f5dd743c84ddec77330b5dcf7e1f69a26ec55e0aa4fe504307b83f7850782510"""

if __name__ == '__main__':
    p2p = P2pClient(silent = False)
    p2p.connect_to('vagrant', 36363)
    p2p.send_msg('wallet')
    #Start getting balance, trans history and pending trans
    denys_public_key = EcdsaHashing.recover_public_key_str(denys_private_key)
    william_public_key = EcdsaHashing.recover_public_key_str(temp_key)
    #william_public_key = '4dc0891733e18601025d2509ea2008661a916078af92237cf4e624ed9aed4419'
    transaction_msg = message.Message('get_user_info', william_public_key)
    transaction_json = transaction_msg.to_json(is_object=False)
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    p2p.send_msg(transaction_json)
    data = p2p.recv_msg()
    print(data)
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


    scontract_test = {"action": "get_signed_contract", "data": {
            "contractFilters": [
                {
                    "type": "signed_contracts:rate",
                    "startRange": .4,
                    "endRange": .5
                },
                {
                    "type": "signed_contracts:amount",
                    "startRange": 50,
                    "endRange": 1000
                }
            ]
        }
    }
    # contract_json = json.dumps(scontract_test, sort_keys=True)
    # p2p.send_msg(contract_json)
    # data = p2p.recv_msg()
    # print(data)
    #quiting
    transaction_msg = message.Message('exit', 'quit')
    transaction_json = transaction_msg.to_json(is_object=False)
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    p2p.send_msg(transaction_json)
    p2p.close_socket()
    #end
