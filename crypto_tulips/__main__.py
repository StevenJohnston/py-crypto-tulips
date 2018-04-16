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
from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.p2p.message import Message
from crypto_tulips.market.exchange_manager import ExchangeManager

from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.block_service import BlockService
from crypto_tulips.services.pos_service import POSService

from crypto_tulips.services.base_object_service import BaseObjectService

from crypto_tulips.dal.services.contract_service import ContractService, ContractFilter
from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.services.signed_contract_service import SignedContractService, SignedContractFilter
from crypto_tulips.dal.objects.signed_contract import SignedContract
from crypto_tulips.services.genesis_block_service import GenesisBlockService
from crypto_tulips.services.contract_transaction_service import ContractTransactionService

from crypto_tulips.miner.miner import Miner

denys_private_key = """4a7351205a7bfaa9726a67cba6f331f1b03ee1e904250f95f81f82e775bb55c1"""

william_private_key = """2b6220b1d8e00a6a95ab943d906cf7fefc4273f01a9b7d7c32b0527638d264f3"""

matt_private_key = """f5dd743c84ddec77330b5dcf7e1f69a26ec55e0aa4fe504307b83f7850782510"""

steven_private_key = """55a1281dfe6cf404816be8f2bb33813e2cf8ef499fb22e21cb090f8f8563a72a"""

naween_private_key = """2276ef4c2368ea0058f9bc73394e4b383f27ff02218968aa4fdc290edda8d803"""


transaction_lock = threading.Lock()
block_lock = threading.Lock()
contract_lock = threading.Lock()

miner_private = steven_private_key

new_block_callbacks = []
block_mine_thread = None
kill_threads = False
def check_if_object_exist(obj_hash, obj_type):
    rs = redis_service.RedisService()
    obj = rs.get_object_by_hash(obj_hash=obj_hash, obj=obj_type)
    if obj is None:
        return False
    return True

def regular_node_callback(data, peer_id=None):
    global kill_threads
    if kill_threads:
        return
    do_block_resend = False
    do_transaction_resend = True
    do_contract_resend = True
    sync_transaction = False
    sync_block = False
    sync_contract = False
    signed_contract_flag = False
    contract_transaction_flag = False
    pos_transaction_flag = False
    json_dic = json.loads(data)
    new_msg = message.Message.from_dict(json_dic)
    # sync block is the same as block, but they don't
    # need to be resend
    if new_msg.action == 'block_sync':
        new_msg.action = 'block'
        do_block_resend = False
        sync_block = True
    elif new_msg.action == 'transaction_sync' or new_msg.action == 'transaction_pos_sync' or new_msg.action == 'transaction_contract_sync':
        if new_msg.action == 'transaction_sync':
            new_msg.action = 'transaction'
        elif new_msg.action == 'transaction_pos_sync':
            new_msg.action = 'transaction_pos'
        elif new_msg.action == 'transaction_contract_sync':
            new_msg.action = 'transaction_contract'
        do_transaction_resend = False
        sync_transaction = True
    elif new_msg.action == 'contract_sync' or new_msg.action == 'contract_signed_sync':
        if new_msg.action == 'contract_sync':
            new_msg.action = 'contract'
        elif new_msg.action == 'contract_signed_sync':
            new_msg.action = 'contract_signed'
        do_contract_resend = False
        sync_contract = True
    # case to set flags for special types of transactions and contracts
    if new_msg.action == 'contract_signed':
        new_msg.action = 'contract'
        signed_contract_flag = True
    elif new_msg.action == 'transaction_contract':
        new_msg.action = 'transaction'
        contract_transaction_flag = True
    elif new_msg.action == 'transaction_pos':
        new_msg.action = 'transaction'
        pos_transaction_flag = True
    if new_msg.action == 'transaction':
        if contract_transaction_flag:
            print('\nContract Transaction')
            new_msg.data = ContractTransaction.from_dict(new_msg.data)
            object_to_check = ContractTransaction
            transaction_action = 'transaction_contract'
        elif pos_transaction_flag:
            print('\nPOS Transaction')
            new_msg.data = PosTransaction.from_dict(new_msg.data)
            object_to_check = PosTransaction
            transaction_action = 'transaction_pos'
        else:
            print('\nNormal Transaction')
            new_msg.data = Transaction.from_dict(new_msg.data)
            object_to_check = Transaction
            transaction_action = 'transaction'
        new_transaction = new_msg.data
        need_to_send = False
        transaction_lock.acquire()
        print('\nTransaction : {}'.format(new_transaction._hash))
        if not check_if_object_exist(new_transaction._hash, object_to_check):
            if a_node.doing_transaction_sync and not sync_transaction:
                a_node.transaction_queue.append(new_transaction)
                print('Added transaction to the queue')
            else:
                rs = redis_service.RedisService()
                rs.store_object(new_transaction)
                need_to_send = True
                print('All good')
        else:
            print('Duplicate transaction')
        transaction_lock.release()
        if need_to_send and do_transaction_resend:
            send_a_transaction(new_transaction, action=transaction_action)
    elif new_msg.action == 'contract':
        if signed_contract_flag:
            print('\nSigned Contract')
            new_msg.data = SignedContract.from_dict(new_msg.data)
            object_to_check = SignedContract
            method_to_call = SignedContractService.store_signed_contract
            contract_action = 'contract_signed'
        else:
            print('\nNormal Contract')
            new_msg.data = Contract.from_dict(new_msg.data)
            object_to_check = Contract
            method_to_call = ContractService.store_contract
            contract_action = 'contract'
        new_contract = new_msg.data
        need_to_send = False
        contract_lock.acquire()
        print('Contract : {}'.format(new_contract._hash))
        if not check_if_object_exist(new_contract._hash, object_to_check):
            if a_node.doing_contract_sync and not sync_contract:
                a_node.contract_queue.append([new_contract, method_to_call])
                print('Added contract to the queue')
            else:
                method_to_call(new_contract)
                need_to_send = True
                print('All good')
        else:
            print('Duplicate contract')
        contract_lock.release()
        if need_to_send and do_contract_resend:
            send_a_contract(new_contract, action=contract_action)
    elif new_msg.action == 'transaction_sync_end':
        print('\n\nFinished transaction sync')
        a_node.doing_transaction_sync = False
        a_node.add_transactions_from_queue()
    elif new_msg.action == 'block_sync_end':
        print('\n\nFinished block sync')
        a_node.doing_blockchain_sync = False
        # after we have added all sync blocks
        # we need to add normal blocks
        # that were send while we where doing sync
        a_node.add_blocks_from_queue()
    elif new_msg.action == 'contract_sync_end':
        print('\n\nFinished contract sync')
        a_node.doing_contract_sync = False
        a_node.add_contracts_from_queue()
    elif new_msg.action == 'init_sync_contract':
        print('Contract sync request')
        mem_contracts = BaseObjectService.get_all_mempool_objects(Contract)
        print('I have {} contracts'.format(len(mem_contracts)))
        mem_signed_contracts = BaseObjectService.get_all_mempool_objects(SignedContract)
        print('I have {} signed contracts'.format(len(mem_signed_contracts)))
        contract_lock.acquire()
        for a_contract in mem_contracts:
            send_a_contract(a_contract, action='contract_sync', contract_target_peer_id=peer_id)
        for a_signed_contract in mem_signed_contracts:
            send_a_contract(a_signed_contract, action='contract_signed_sync', contract_target_peer_id=peer_id)
        ending_msg = message.Message(action='contract_sync_end', data='')
        json_dic = ending_msg.to_json(is_object=False)
        json_str = json.dumps(json_dic, sort_keys=True, separators=(',', ':'))
        a_node.connection_manager.send_msg(msg=json_str, target_peer_id=peer_id)
        contract_lock.release()
    elif new_msg.action == 'init_sync_trans':
        print('Transaction sync request')
        mem_transactions = TransactionService.get_all_mempool_transactions()
        print('I have {} mem transactions'.format(len(mem_transactions)))
        mem_pos_transactions = BaseObjectService.get_all_mempool_objects(PosTransaction)
        print('I have {} mem pos transactions'.format(len(mem_pos_transactions)))
        mem_contract_transactions = BaseObjectService.get_all_mempool_objects(ContractTransaction)
        print('I have {} mem contract transactions'.format(len(mem_contract_transactions)))
        transaction_lock.acquire()
        for a_transaction in mem_transactions:
            send_a_transaction(a_transaction, action='transaction_sync', transaction_target_peer_id=peer_id)
        for a_pos_transaction in mem_pos_transactions:
            send_a_transaction(a_pos_transaction, action='transaction_pos_sync', transaction_target_peer_id=peer_id)
        for a_contract_transaction in mem_contract_transactions:
            send_a_transaction(a_contract_transaction, action='transaction_contract_sync', transaction_target_peer_id=peer_id)
        ending_msg = message.Message(action='transaction_sync_end', data='')
        json_dic = ending_msg.to_json(is_object=False)
        json_str = json.dumps(json_dic, sort_keys=True, separators=(',', ':'))
        a_node.connection_manager.send_msg(msg=json_str, target_peer_id=peer_id)
        transaction_lock.release()
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

        bs = dal_service_block_service.BlockService()

        need_to_send = False
        need_to_mine_new = False
        block_lock.acquire()
        print('\nBlock : {}'.format(new_block._hash))
        # if the node is doing blockchain sync
        # and this block is not sync block
        # we need to add it to the queue
        if a_node.doing_blockchain_sync and not sync_block:
            a_node.block_queue.append(new_block)
            result_list = []
        else:
            if Miner.validate_incoming_block(new_block):
                result_list = block_service.add_block_to_chain(new_block)
                if result_list:
                    need_to_mine_new = True
            else:
                result_list = []
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

        if need_to_mine_new:
            for new_block_callback in new_block_callbacks:
                new_block_callback(new_block)

def run_miner():
    print('starting miner')
    new_block_callbacks.append(mine_block)
    last_block_hash = BlockService.get_last_block_hash()
    block_service_dal = dal_service_block_service.BlockService()
    last_block = block_service_dal.find_by_hash(last_block_hash)
    mine_block(last_block)

def mine_block(last_block):
    global kill_threads
    if kill_threads:
        return
    if last_block:
        print('mining off last block ' + last_block._hash)
    else:
        print('Creating genisis')
        last_block = GenesisBlockService.generate_from_priv(miner_private)
        block_service_dal = dal_service_block_service.BlockService()
        block_lock.acquire()
        block_service_dal.store_block(last_block)
        block_lock.release()
        send_a_block(last_block)

    # check if we are the miner.
    miner_pub = EcdsaHashing.recover_public_key_str(miner_private)
    next_author = POSService.get_next_block_author(last_block)
    print('me: ' + str(miner_pub))
    print('author: ' + str(next_author))
    print(next_author == miner_pub)
    if next_author == miner_pub:
        block = Miner.mine_block(miner_private, last_block)
        block_lock.acquire()
        BlockService.add_block_to_chain(block)
        block_lock.release()
        print('\nCreated Block hash: ' + block._hash)
        send_a_block(block)
        global block_mine_thread
        block_mine_thread = threading.Timer(30, mine_block, [block])
        block_mine_thread.start()

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
            user_trans_history, transaction_balance = TransactionService.get_transactions_by_public_key(new_msg.data, True)
            balances = BlockService.get_all_balances()
            user_balance = balances.get(new_msg.data, 0)
            for trans in user_trans_history:
                if(trans.is_mempool == 1):
                    pending.append(trans.get_sendable())
                else:
                    transaction.append(trans.get_sendable())
            string_user_info_json = build_return_json([("pending", pending), ("transaction", transaction), ("amount", user_balance)])
            #print(string_user_info_json)
            a_node.connection_manager.server.send_msg(data=string_user_info_json, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == 'send_tx':
            t = Transaction.from_dict(new_msg.data)
            trans_signable = t.get_signable()
            trans_signable_json = json.dumps(trans_signable, sort_keys=True, separators=(',', ':'))
            status = EcdsaHashing.verify_signature_hex(t.from_addr, t.signature, trans_signable_json)
            if status == True:
                rs = redis_service.RedisService()
                transaction_lock.acquire()
                rs.store_object(t)
                transaction_lock.release()
                send_a_transaction(t)
                a_node.connection_manager.server.send_msg(data="Transaction Successful", client_socket=wallet_sock)
            else:
                a_node.connection_manager.server.send_msg(data="Transaction Failed", client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == 'send_ctx':
            ctx = ContractTransaction.from_dict(new_msg.data)
            trans_signable = ctx.get_signable()
            trans_signable_json = json.dumps(trans_signable, sort_keys=True, separators=(',', ':'))
            status = EcdsaHashing.verify_signature_hex(ctx.from_addr, ctx.signature, trans_signable_json)
            if status == True:
                rs = redis_service.RedisService()
                transaction_lock.acquire()
                rs.store_object(ctx)
                transaction_lock.release()
                send_a_transaction(ctx, action='transaction_contract')
                a_node.connection_manager.server.send_msg(data="Contract Transaction Successful", client_socket=wallet_sock)
                a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
            else:
                a_node.connection_manager.server.send_msg(data="Contract Transaction Failed", client_socket=wallet_sock)
        elif new_msg.action == "get_all_ip":
            node_obj_list = a_node.connection_manager.peer_list
            ip_list = [node.get_ip_address() for node in node_obj_list]
            json_ip_list_str_return = build_return_json([("ipaddress_list", ip_list)])
            print(json_ip_list_str_return)
            a_node.connection_manager.server.send_msg(data=json_ip_list_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == "get_contracts":
            contracts_filter = get_contracts_list(new_msg.data)
            contracts = ContractService.get_contracts_by_filter(contracts_filter, False)
            new_contracts = [contract.get_sendable() for contract in contracts]
            json_str_return = build_return_json([("available_contracts", new_contracts)])
            a_node.connection_manager.server.send_msg(data=json_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == "get_signed_contracts":
            signed_contracts_filter = get_contracts_list(new_msg.data, contract_type=2)
            signed_contracts = SignedContractService.get_signed_contracts_by_filter(signed_contracts_filter, False)
            new_signed_contracts = [contract.get_sendable() for contract in signed_contracts]
            json_str_return = build_return_json([("signed_contracts", new_signed_contracts)])
            a_node.connection_manager.server.send_msg(data=json_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == "publish_contract":
            c = Contract.from_dict(new_msg.data)
            contract_signable_json = c.get_signable()
            contract_signable_json_str = json.dumps(contract_signable_json, sort_keys=True, separators=(',', ':'))
            status = EcdsaHashing.verify_signature_hex(c.owner, c.signature, contract_signable_json_str)
            if status == True:
                contract_lock.acquire()
                ContractService.store_contract(c)
                contract_lock.release()
                send_a_contract(c)
                a_node.connection_manager.server.send_msg(data="Contract Successfully Created", client_socket=wallet_sock)
                a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
            else:
                a_node.connection_manager.server.send_msg(data="Contract Cannot be created", client_socket=wallet_sock)
        elif new_msg.action == "subscribe_to_contract":
            sc = SignedContract.from_dict(new_msg.data)
            signed_contract_signable_json = sc.get_signable()
            signed_contract_signable_json_str = json.dumps(signed_contract_signable_json, sort_keys=True, separators=(',', ':'))
            status = EcdsaHashing.verify_signature_hex(sc.from_addr, sc.signature, signed_contract_signable_json_str)
            if status == True:
                contract_lock.acquire()
                SignedContractService.store_signed_contract(sc)
                contract_lock.release()
                send_a_contract(sc, action='contract_signed')
                a_node.connection_manager.server.send_msg(data="Successfully Subscribed", client_socket=wallet_sock)
                a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
            else:
                a_node.connection_manager.server.send_msg(data="Cannot Subscribed", client_socket=wallet_sock)
        #the a list of user inside your contracts
        elif new_msg.action == "get_all_user_partipation_contract":
            user_contracts_sub = SignedContractService.get_all_signed_contracts_by_owner(new_msg.data["userPartipication"])
            new_user_contracts_sub = [contract.get_sendable() for contract in user_contracts_sub]
            json_str_return = build_return_json([("contract_subscription", new_user_contracts_sub)])
            a_node.connection_manager.server.send_msg(data=json_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
            pass
        #The user contract that they created
        elif new_msg.action == "get_user_contracts":
            all_contract = ContractService.get_all_contracts_by_owner(new_msg.data["userPublicKey"])
            new_contracts = [contract.get_sendable() for contract in all_contract]
            json_str_return = build_return_json([("contract_owned", new_contracts)])
            a_node.connection_manager.server.send_msg(data=json_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == "get_bitcoin_price":
            rs = redis_service.RedisService()
            r = rs._connect()
            price_time = r.zrange('price_stamps', -1, -1, withscores=True)
            price = float(price_time[0][0])
            height = BlockService.get_max_height()
            json_str_return = build_return_json([("bitcoinPrice", str(price)), ("height", str(height))])
            a_node.connection_manager.server.send_msg(data=json_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == "get_contract_subscription":
            scs = SignedContractService.get_all_signed_contracts_by_from_addr(new_msg.data["userPublicKey"])
            new_contracts = [contract.get_sendable() for contract in scs]
            json_str_return = build_return_json([("user_contract_subscription", new_contracts)])
            a_node.connection_manager.server.send_msg(data=json_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == "get_contracts_and_signed_contract_info":
            balances = BlockService.get_all_balances()
            #all contract owned
            all_contract = ContractService.get_all_contracts_by_owner(new_msg.data["userPublicKey"])
            all_contracts_str = [contract.get_sendable() for contract in all_contract]
            #signed contract
            signed_contracts_sub = SignedContractService.get_all_signed_contracts_by_owner(new_msg.data["userPublicKey"])
            signed_contracts_sub_str = [contract.get_sendable() for contract in signed_contracts_sub]
            # balances
            new_dict = {}
            for signed_contract in signed_contracts_sub:
                b = balances.get(signed_contract._hash, (0,0))
                new_dict[signed_contract._hash] = b
            #history
            contract_transaction_history = ContractTransactionService.get_contract_transactions_from_public_key(new_msg.data["userPublicKey"], False)
            contract_transaction_history_str = [contract.get_sendable() for contract in contract_transaction_history]
            json_str_return = build_return_json([("contract_owned", all_contracts_str), ("contract_subscription", signed_contracts_sub_str), ("transaction_history", contract_transaction_history_str), ('balances', new_dict)])
            a_node.connection_manager.server.send_msg(data=json_str_return, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == "get_signed_by_contract_hash":
            # signed contracts
            signed_contracts = SignedContractService.get_all_signed_contracts_by_contract_hash(new_msg.data['_hash'])
            signed_contracts_str = [sc.get_sendable() for sc in signed_contracts]
            # contract
            contract = ContractService.get_contract_by_hash(new_msg.data['_hash'])
            contract_str = contract.get_sendable()

            json_str = build_return_json([('contract', contract_str), ('signed_contracts', signed_contracts_str)])
            a_node.connection_manager.server.send_msg(data=json_str, client_socket=wallet_sock)
            a_node.connection_manager.server.send_msg(data="end", client_socket=wallet_sock)
        elif new_msg.action == 'exit':
            break
        else:
            a_node.connection_manager.server.send_msg(data="Bad Data", client_socket=wallet_sock)
    a_node.connection_manager.server.close_client(client_socket=wallet_sock)

def parse_contract_filter(contract):
    return contract["type"], contract["startRange"], contract["endRange"]


def build_return_json(list_of_pair):
    data = {}
    for key, value in list_of_pair:
        data[key] = value
    return json.dumps(data)

def get_contracts_list(dict_data, contract_type=1):
    contracts_filter = []
    contracts_json_str = json.dumps(dict_data, sort_keys=True, separators=(',', ':'))
    json_contract_list = json.loads(contracts_json_str)
    for json_contract in json_contract_list["contractFilters"]:
        type_filter, start_range, end_range = parse_contract_filter(json_contract)
        if contract_type == 1:
            cf = ContractFilter(type_filter, start_range, end_range)
        else:
            cf = SignedContractFilter(type_filter, start_range, end_range)
        contracts_filter.append(cf)
    return contracts_filter


def send_a_transaction(new_transaction, action='transaction', transaction_target_peer_id=None):
    transaction_msg = message.Message(action, new_transaction)
    transaction_json = transaction_msg.to_json()
    transaction_json = json.dumps(transaction_json, sort_keys=True, separators=(',', ':'))
    a_node.connection_manager.send_msg(msg=transaction_json, target_peer_id=transaction_target_peer_id)

def send_a_contract(new_contract, action='contract', contract_target_peer_id=None):
    contract_msg = message.Message(action, new_contract)
    contract_json = contract_msg.to_json()
    contract_json = json.dumps(contract_json, sort_keys=True, separators=(',', ':'))
    a_node.connection_manager.send_msg(msg=contract_json, target_peer_id=contract_target_peer_id)

def start_as_regular(bootstrap_host, peer_timeout=0, recv_data_size=2048, \
        socket_timeout=1):
    print('\t\tStarting as a regular node')
    global a_node
    global miner_private
    a_node = node.Node()
    a_node.join_network(bootstrap_host, peer_timeout=peer_timeout, recv_data_size=recv_data_size, \
            socket_timeout=socket_timeout, read_callback=regular_node_callback, wallet_callback=wallet_callback, \
            start_bootstrap=True, start_gossiping=True)
    a_node.make_silent(True)
    # need to have a way to shut it down
    # right now when trying to exit this just hangs
    exchange_manager = ExchangeManager()
    while True:
        user_input = input('\t\t\tEnter a command: ')
        if user_input == 'quit' or user_input == 'q':
            try:
                global kill_threads
                global block_mine_thread
                kill_threads = True
                exchange_manager.stop()
                if block_mine_thread is not None:
                    block_mine_thread.cancel()
            except Exception as ex:
                print('Error during quick, {}'.format(str(ex)))
            break
        elif user_input == 'height':
            try:
                print('Blocks {}'.format(BlockService.get_max_height()))
                print('Mem Transactions {}'.format(len(TransactionService.get_all_mempool_transactions())))
                print('Mem POS Transactions {}'.format(len(BaseObjectService.get_all_mempool_objects(PosTransaction))))
                print('Mem Contract Transactions {}'.format(len(BaseObjectService.get_all_mempool_objects(ContractTransaction))))
                print('Mem Contracts {}'.format(len(BaseObjectService.get_all_mempool_objects(Contract))))
                print('Mem Signed Contracts {}'.format(len(BaseObjectService.get_all_mempool_objects(SignedContract))))
            except Exception as ex:
                print('Error during height calculation, {}'.format(str(ex)))
        elif user_input == 'test':
            pass
        elif user_input == 'who':
            print('Current miner is {}'.format(miner_private))
        elif user_input == 'miner' or user_input == 'm':
            try:
                run_miner()
            except Exception as ex:
                print('Error during starting miner, {}'.format(str(ex)))
        elif user_input == 'priv' or user_input == 'p':
            try:
                secret = input('\t\t\tNew miner : ')
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
                    private_key = secret
                miner_private = private_key
            except Exception as ex:
                print("Error during miner's private key change, {}".format(str(ex)))

        elif user_input == 'balances' or user_input == 'b':
            try:
                balances = BlockService.get_all_balances()
                print(balances)
            except Exception as ex:
                print('Error during balance calculation, {}'.format(str(ex)))

        elif user_input == 'signed contract' or user_input == 'sc':
            try:
                contract_addr = input('\t\t\tContract Hash : ')
                a_contract = ContractService.get_contract_by_hash(contract_addr)
                print('contract hash = ' + a_contract._hash)

                secret = input('\t\t\tSignee : ')
                a_signed_contract = SignedContract('', '', \
                        sc_from_addr='', signed_timestamp=time.time(), \
                        parent_hash='', parent_signature='', parent_owner='', \
                        amount=10, rate=0.2, is_mempool=1, duration=60, \
                        created_timestamp=time.time(), sign_end_timestamp=time.time() + 1000)
                #        created_timestamp=time.time(), sign_end_timestamp=time.time() + 1000)
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
            # a_contract.owner = EcdsaHashing.recover_public_key_str(steven_private_key)
            # a_contract.update_signature(steven_private_key)
            # a_contract.update_hash()

                a_signed_contract.from_addr = EcdsaHashing.recover_public_key_str(private_key)
                a_signed_contract.parent_hash = a_contract._hash
                a_signed_contract.parent_signature = a_contract.signature
                a_signed_contract.parent_owner = a_contract.owner
                a_signed_contract.amount = a_contract.amount
                a_signed_contract.rate = a_contract.rate
                a_signed_contract.duration = a_contract.duration
                a_signed_contract.created_timestamp = a_contract.created_timestamp
                a_signed_contract.sign_end_timestamp = a_contract.sign_end_timestamp
                a_signed_contract.update_signature(private_key)
                a_signed_contract.update_hash()
                send_a_contract(a_signed_contract, action='contract_signed')
                contract_lock.acquire()
                SignedContractService.store_signed_contract(a_signed_contract)
                contract_lock.release()
                print('\nSigned Contract hash : {}'.format(a_signed_contract._hash))
            except Exception as ex:
                print('Error during signed contract creation, {}'.format(str(ex)))

        elif user_input == 'contract' or user_input == 'c':
            try:
                secret = input('\t\t\tOwner : ')
                a_contract = Contract('', '', owner='', amount=10, \
                        rate=0.2, is_mempool=1, duration=60, \
                        created_timestamp=time.time(), sign_end_timestamp=time.time() + 240000)
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
                a_contract.owner = EcdsaHashing.recover_public_key_str(private_key)
                a_contract.update_signature(private_key)
                a_contract.update_hash()
                send_a_contract(a_contract)
                contract_lock.acquire()
                ContractService.store_contract(a_contract)
                contract_lock.release()
                print('\nContract hash : {}'.format(a_contract._hash))
            except Exception as ex:
                print('Error during contract creation, {}'.format(str(ex)))

        elif user_input == 'contract transaction' or user_input == 'ct':
            try:
                rs = redis_service.RedisService()
                signed_contract_hash = input('\t\t\tSigned Contract Hash : ')
                signed_contract = SignedContractService.get_signed_contract_by_hash(signed_contract_hash)
                owner = input('\t\t\tOwner: ')

                to_symbol = input('\t\t\tTo TPS or BTC: ')
                from_symbol = input('\t\t\tFrom TPS or BTC: ')
                amount = input('\t\t\tAmount: ')

                if owner == 'denys' or owner == 'd':
                    private_key = denys_private_key
                elif owner == 'william' or owner == 'will' or owner == 'w':
                    private_key = william_private_key
                elif owner == 'matt' or owner == 'm':
                    private_key = matt_private_key
                elif owner == 'steven' or owner == 's':
                    private_key = steven_private_key
                elif owner == 'naween' or owner == 'n':
                    private_key = naween_private_key
                else:
                    continue
            # public_key = EcdsaHashing.recover_public_key_str(private_key)
            # a_contract_transaction = ContractTransaction('', '', public_key, \
            #         'sc_contract_addr', 'BTC', 'TPS', 10, 1, time.time())
            # a_contract_transaction.price = 6000
            # a_contract_transaction.update_signature(private_key)
            # a_contract_transaction.update_hash()
                r = rs._connect()
                time_price = r.zrange('price_stamps', -1, -1, withscores=True)
                price = float(time_price[0][0])
                a_contract_transaction = ContractTransaction('', '', signed_contract.parent_owner, signed_contract._hash, to_symbol, from_symbol, amount, price, 1)
                a_contract_transaction.update_signature(private_key)
                a_contract_transaction.update_hash()
                send_a_transaction(a_contract_transaction, action='transaction_contract')
                transaction_lock.acquire()

                rs.store_object(a_contract_transaction)
                transaction_lock.release()
                print('\nContract Transaction hash : {}'.format(a_contract_transaction._hash))
            except Exception as ex:
                print('Error during contract transaction creation, {}'.format(str(ex)))

        elif user_input == 'pos' or user_input == 'pos_transaction' or user_input == 'pt':
            try:
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
                    private_key = secret
                public_key = EcdsaHashing.recover_public_key_str(private_key)
                amount = input('\t\t\tAmount: ')
                pos_transaction = PosTransaction('', '', public_key, amount, 1)
                pos_transaction.update_signature(private_key)
                pos_transaction.update_hash()
                # send pos_transaction
                send_a_transaction(pos_transaction, action='transaction_pos')
                print('\nPOS Transaction hash : {}'.format(pos_transaction._hash))

                transaction_lock.acquire()
                rs = redis_service.RedisService()
                rs.store_object(pos_transaction)
                transaction_lock.release()
            except Exception as ex:
                print('Error during pos transaction creation, {}'.format(str(ex)))


        elif user_input == 'trans' or user_input == 'transaction' or user_input == 't':
            try:
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
                    private_key = secret
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
                    # to_addr is already a given public key, no need to calculate it
                    pass
                    #to_addr = EcdsaHashing.recover_public_key_str(to_addr)
                from_addr = public_key
                amount = input('\t\t\tAmount: ')
                new_transaction = Transaction('', '', to_addr, from_addr, amount, 1)
                new_transaction.update_signature(private_key)
                new_transaction.update_hash()
                send_a_transaction(new_transaction)
                transaction_lock.acquire()
                print('\nTransaction hash : {}'.format(new_transaction._hash))
                rs = redis_service.RedisService()
                rs.store_object(new_transaction)
                transaction_lock.release()
            except Exception as ex:
                print('Error during transaction creation, {}'.format(str(ex)))
    a_node.close()

if __name__ == '__main__':
    arguments = sys.argv[1:]
    if not arguments:
        host = socket.gethostbyname(socket.getfqdn())
    else:
        host = arguments[0]
    start_as_regular(host)
