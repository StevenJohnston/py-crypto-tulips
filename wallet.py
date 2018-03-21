from crypto_tulips.p2p.p2p_client import P2pClient
from crypto_tulips.p2p import message
from crypto_tulips.hashing.crypt_hashing import Hashing
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
    denys_public_key = Hashing.get_public_key(denys_private_key)
    william_public_key = Hashing.get_public_key(william_private_key)
    transaction_msg = message.Message('tx_by_public_key', william_public_key)
    transaction_json = transaction_msg.to_json(is_object=False)
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    p2p.send_msg(transaction_json)
    data = p2p.recv_msg()
    #ends

    #Testing user wallet key generation
    #public_key = Hashing.get_public_key(temp)
    # print(public_key)
    # sig = Hashing.str_signature_of_data('message', temp)
    # print(sig)
    #ends user wallet testing

    #start a transaction
    amount = 100
    new_transaction = Transaction('', '', denys_public_key, william_public_key, amount, 1)
    new_transaction.update_signature(william_private_key)
    new_transaction.update_hash()

    transaction_msg = message.Message('tx', new_transaction)
    transaction_json = transaction_msg.to_json()
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    print(transaction_json)
    p2p.send_msg(transaction_json)
    data = p2p.recv_msg()

    #quiting
    transaction_msg = message.Message('exit', 'quit')
    transaction_json = transaction_msg.to_json(is_object=False)
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    p2p.send_msg(transaction_json)
    p2p.close_socket()
    #end
