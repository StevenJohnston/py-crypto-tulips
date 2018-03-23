"""
Script that is getting executed when running crypto_tulips
"""
import sys
import json
import time
import socket
import threading
from .dal.services import redis_service
from .node import node
from .p2p import message
from .hashing.crypt_hashing_wif import EcdsaHashing
from crypto_tulips.dal.services import block_service as dal_service_block_service
from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.p2p.message import Message

from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.block_service import BlockService
from crypto_tulips.services.pos_service import POSService

from crypto_tulips.services.base_object_service import BaseObjectService

denys_private_key = """55a1281dfe6cf404816be8f2bb33813e2cf8ef499fb22e21cb090f8f8563a72a"""

william_private_key = """83c82312b925e50dde81f57f88f2fe1fb8310de1d81e97b696235c6093cd6af8"""

matt_private_key = """f5dd743c84ddec77330b5dcf7e1f69a26ec55e0aa4fe504307b83f7850782510"""

steven_private_key = """4a7351205a7bfaa9726a67cba6f331f1b03ee1e904250f95f81f82e775bb55c1"""

naween_private_key = """418a3147a90f519cd72fb05eb2f201368ee7265f36efb8824e9daed59aabe9e0"""

transaction_lock = threading.Lock()
block_lock = threading.Lock()

new_block_callbacks = []
def check_if_object_exist(obj_hash, obj_type):
    rs = redis_service.RedisService()
    obj = rs.get_object_by_hash(obj_hash=obj_hash, obj=obj_type)
    #obj = rs.get_object_by_full_key(obj_key=obj_hash, obj=obj_type)
    if obj is None:
        return False
    return True

def regular_node_callback(data, peer_id=None):
    do_block_resend= True
    sync_block = False
    json_dic = json.loads(data)
    new_msg = message.Message.from_dict(json_dic)
    # sync block is the same as block, but they don't
    # need to be resend
    if new_msg.action == 'block_sync':
        new_msg.action = 'block'
        do_block_resend = False
        sync_block = True
    if new_msg.action == 'transaction':
        new_msg.data = Transaction.from_dict(new_msg.data)
        new_transaction = new_msg.data
        need_to_send = False
        transaction_lock.acquire()
        print('\nTransaction : {}'.format(new_transaction._hash))
        if not check_if_object_exist(new_transaction._hash, Transaction):
            rs = redis_service.RedisService()
            rs.store_object(new_transaction)
            need_to_send = True
            print('All good')
        else:
            print('Duplicate transaction')
        transaction_lock.release()
        if need_to_send:
            send_a_transaction(new_transaction)
    elif new_msg.action == 'block_sync_end':
        a_node.doing_blockchain_sync = False
        # after we have added all sync blocks
        # we need to add normal blocks
        # that were send while we where doing sync
        a_node.add_blocks_from_queue()
    elif new_msg.action == 'init_sync':
        print('\nGot init sync, height is {}'.format(new_msg.data))
        peer_height = new_msg.data
        my_height = BlockService.get_max_height()
        # only do sync if we need to send blocks to a peer
        if peer_height < my_height:
            print('My height is higher, {}'.format(my_height))
            bs = dal_service_block_service.BlockService()
            list_of_blocks = bs.get_blocks_after_height(peer_height)
            block_lock.acquire()
            for a_block in list_of_blocks:
                send_a_block(a_block, action='block_sync', block_target_peer_id=peer_id)
            ending_msg = message.Message(action='block_sync_end', data='')
            json_dic = ending_msg.to_json(is_object=False)
            json_str = json.dumps(json_dic, sort_keys=True, separators=(',', ':'))
            a_node.connection_manager.send_msg(msg=json_str, target_peer_id=peer_id)
            block_lock.release()
        else:
            print('Same height')
            ending_msg = message.Message(action='block_sync_end', data='')
            json_dic = ending_msg.to_json(is_object=False)
            json_str = json.dumps(json_dic, sort_keys=True, separators=(',', ':'))
            a_node.connection_manager.send_msg(msg=json_str, target_peer_id=peer_id)
    elif new_msg.action == 'block':
        block_service = BlockService()
        new_block = Block.from_dict(new_msg.data)
        need_to_send = False
        block_lock.acquire()
        print('\nBlock : {}'.format(new_block._hash))
        # if the node is doing blockchain sync
        # and this block is not sync block
        # we need to add it to the queue
        if a_node.doing_blockchain_sync and not sync_block:
            a_node.block_queue.append(new_block)
            result_list = []
        else:
            result_list = block_service.add_block_to_chain(new_block)
            for new_block_callback in new_block_callbacks: 
                new_block_callback(new_block)
        if result_list:
            need_to_send = True
            print('All good')
        else:
            if a_node.doing_blockchain_sync and not sync_block:
                print('Added block to a queue')
            else:
                print('Duplicate block')
        block_lock.release()
        if need_to_send and do_block_resend:
            send_a_block(new_block)

def run_miner():
    new_block_callbacks.append(mine_block)
    
def mine_block(last_block):
    # check if we are the miner. 
    steven_pub = EcdsaHashing.recover_public_key_str(steven_private_key)
    next_author = POSService.get_next_block_author(last_block)
    if next_author == steven_pub:
        block_service = BlockService()
        time_now = int(time.time())
        #height = int(BlockService.get_max_height()) + 1
        height = last_block.height + 1
        ten_transactions = TransactionService.get_10_transactions_from_mem_pool()
        #last_block_hash = BlockService.get_last_block_hash()
        last_block_hash = last_block._hash
        block = Block('', '', steven_pub, last_block_hash, height, ten_transactions, [], [], [], [], time_now)
        block.update_signature(steven_private_key)
        block.update_hash()
        block_lock.acquire()
        block_service.add_block_to_chain(block)
        # TODO Test if worked block was added. Might fail due to same hash
        for trabs in ten_transactions:
            BaseObjectService.remove_from_mem_pool(trabs)
        print('\nCreated Block hash: ' + block._hash)
        block_lock.release()
        send_a_block(block)

def send_a_block(new_block, action='block', block_target_peer_id=None):
    block_msg = message.Message(action, new_block)
    sendable_block = block_msg.to_json()
    block_json = json.dumps(sendable_block, sort_keys=True, separators=(',', ':'))
    a_node.connection_manager.send_msg(msg=block_json, target_peer_id=block_target_peer_id)

a_node = None

def wallet_callback(wallet_sock):
    while True:
        data = a_node.connection_manager.server.recv_msg(client_socket=wallet_sock)
        json_dic = json.loads(data)
        new_msg = message.Message.from_dict(json_dic)
        print(new_msg.action)
        if new_msg.action == 'get_user_info':
            pending = []
            transaction = []
            user_trans_history, user_balance = TransactionService.get_transactions_by_public_key(new_msg.data, True)
            for trans in user_trans_history:
                if(trans.is_mempool == 1):
                    pending.append(trans.get_sendable())
                else:
                    transaction.append(trans.get_sendable())
            user_info_json = {
                "pending" : pending,
                "transaction": transaction,
                "amount": user_balance
            }
            string_user_info_json = json.dumps(user_info_json)
            a_node.connection_manager.server.send_msg(data=string_user_info_json, client_socket=wallet_sock)
        elif new_msg.action == 'send_tx':
            t = Transaction.from_dict(new_msg.data)
            trans_signable = t.get_signable()
            trans_signable_json = json.dumps(trans_signable, sort_keys=True, separators=(',', ':'))
            status = EcdsaHashing.verify_signature_hex(t.from_addr, t.signature, trans_signable_json)
            if status == True:
                rs = redis_service.RedisService()
                rs.store_object(t)
                a_node.connection_manager.server.send_msg(data="Transaction Successful", client_socket=wallet_sock)
            else:
                a_node.connection_manager.server.send_msg(data="Transaction Failed", client_socket=wallet_sock)
        elif new_msg.action == "get_all_ip":
            node_obj_list = a_node.connection_manager.peer_list
            ip_list = [node.get_ip_address() for node in node_obj_list]
            ip_list_json = {
                "ipaddress_list" : ip_list
            }
            string_ip_list_json = json.dumps(ip_list_json)
            print(string_ip_list_json)
            a_node.connection_manager.server.send_msg(data=string_ip_list_json, client_socket=wallet_sock)
        elif new_msg.action == 'exit':
            break
        else:
            a_node.connection_manager.server.send_msg(data="Bad Data", client_socket=wallet_sock)
    a_node.connection_manager.server.close_client(client_socket=wallet_sock)

def send_a_transaction(new_transaction):
    transaction_msg = message.Message('transaction', new_transaction)
    transaction_json = transaction_msg.to_json()
    transaction_json = json.dumps(transaction_json, sort_keys=True, separators=(',', ':'))
    a_node.connection_manager.send_msg(msg=transaction_json)

def start_as_regular(bootstrap_host, peer_timeout=0, recv_data_size=2048, \
        socket_timeout=1):
    print('\t\tStarting as a regular node')
    global a_node
    a_node = node.Node()
    a_node.join_network(bootstrap_host, peer_timeout=peer_timeout, recv_data_size=recv_data_size, \
            socket_timeout=socket_timeout, read_callback=regular_node_callback, wallet_callback=wallet_callback, \
            start_bootstrap=True, start_gossiping=True)
    a_node.make_silent(True)
    while True:
        user_input = input('\t\t\tEnter a command: ')
        if user_input == 'quit' or user_input == 'q':
            break
        elif user_input == 'height':
            print(BlockService.get_max_height())
        elif user_input == 'test':
            max_height = BlockService.get_max_height()
            print('\n{}'.format(max_height))
        elif user_input == 'miner' or user_input == 'm':
            run_miner()
        elif user_input == 'trans' or user_input == 'transaction' or user_input == 't':
            secret = input('\t\t\tFrom : ')
            if secret == 'denys' or secret == 'd':
                private_key = denys_private_key
            elif secret == 'william' or secret == 'will' or secret == 'w':
                private_key = william_private_key
            elif secret == 'matt' or secret == 'm':
                private_key = matt_private_key
            elif secret == 'steven' or secret == 's':
                private_key = steven_private_key
            elif secret == 'naween' or secret == 'n':
                private_key = naween_private_key
            else:
                continue
            public_key = EcdsaHashing.recover_public_key_str(private_key)
            to_addr = input('\t\t\tTo addr: ')
            if to_addr == 'denys' or to_addr == 'd':
                to_addr = EcdsaHashing.recover_public_key_str(denys_private_key)
            elif to_addr == 'william' or to_addr == 'w' or to_addr == 'will':
                to_addr = EcdsaHashing.recover_public_key_str(william_private_key)
            elif to_addr == 'matt' or to_addr == 'm':
                to_addr = EcdsaHashing.recover_public_key_str(matt_private_key)
            elif to_addr == 'steven' or to_addr == 's':
                to_addr = EcdsaHashing.recover_public_key_str(steven_private_key)
            elif to_addr == 'naween' or to_addr == 'n':
                to_addr = EcdsaHashing.recover_public_key_str(naween_private_key)
            else:
                continue
            from_addr = public_key
            amount = input('\t\t\tAmount: ')
            new_transaction = Transaction('', '', to_addr, from_addr, amount, 1)
            new_transaction.update_signature(private_key)
            new_transaction.update_hash()
            #transaction_lock.acquire()
            send_a_transaction(new_transaction)
            transaction_lock.acquire()
            print('\nTransaction hash : {}'.format(new_transaction._hash))
            rs = redis_service.RedisService()
            rs.store_object(new_transaction)
            transaction_lock.release()
    a_node.close()

if __name__ == '__main__':
    arguments = sys.argv[1:]
    if not arguments:
        host = socket.gethostbyname(socket.getfqdn())
    else:
        host = arguments[0]
    start_as_regular(host)
