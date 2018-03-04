import sys
import json
from .dal.services import redis_service
from .dal.objects import mem_transaction
from .node import bootstrap, node
from .p2p import message

def start_as_a_bootstrap(bootstrap_port):
    print('\t\tStarting as a bootstrap node at port {}'.format(bootstrap_port))
    bootstrap_node = bootstrap.BootstrapNode(port=bootstrap_port)
    bootstrap_node.accept(True)
    while True:
        user_input = input('\t\t\tEnter a command: ')
        if user_input == 'quit':
            break
    bootstrap_node.close()

def regular_node_callback(data):
    json_dic = json.loads(data)
    new_msg = message.Message.from_dict(json_dic)
    if new_msg.action == 'transaction':
        new_msg.data = mem_transaction.MemTransaction.from_dict(new_msg.data)
        new_transaction = new_msg.data
        print(new_transaction._hash)
        rs = redis_service.RedisService()
        rs.store_object(new_transaction)

def run_miner():
    pass

def start_as_regular(bootstrap_port, bootstrap_host, node_port, peer_timeout=0, recv_data_size=2048, \
        socket_timeout=1):
    print('\t\tStarting as a regular node')
    a_node = node.Node(node_port)
    a_node.join_network(bootstrap_host, bootstrap_port, peer_timeout=peer_timeout, recv_data_size=recv_data_size, \
            socket_timeout=socket_timeout, read_callback=regular_node_callback)
    a_node.make_silent(True)
    while True:
        user_input = input('\t\t\tEnter a command: ')
        if user_input == 'quit':
            break
        elif user_input == 'msg':
            msg_input = input('\t\t\tEnter a msg to send: ')
            if msg_input != '':
                a_node.connection_manager.send_msg(msg=msg_input)
        elif user_input == 'miner':
            run_miner()
        elif user_input == 'trans' or user_input == 'transaction':
            to_addr = input('\t\t\tTo addr: ')
            from_addr = input('\t\t\tFrom addr: ')
            amount = input('\t\t\tAmount: ')
            new_transaction = mem_transaction.MemTransaction('', '', to_addr, from_addr, amount)
            new_transaction.update_hash()
            transaction_msg = message.Message('transaction', new_transaction)
            transaction_json = transaction_msg.to_json()
            transaction_json = json.dumps(transaction_json)
            a_node.connection_manager.send_msg(msg=transaction_json)
            print(new_transaction._hash)
            rs = redis_service.RedisService()
            rs.store_object(new_transaction)
    a_node.close()

if __name__ == '__main__':
    arguments = sys.argv[1:]
    print('\tCommand line arguments are {}'.format(arguments))
    if arguments:
        print('\tGot arguments')
        if arguments[0] == 'bootstrap':
            port = int(arguments[1])
            start_as_a_bootstrap(port)
        elif arguments[0] == 'regular':
            port = int(arguments[1])
            host = arguments[2]
            port_node = int(arguments[3])
            start_as_regular(port, host, port_node)
    else:
        print('Arguments:')
        print('\tbootstrap -- bootstrap mode')
        print('\t\t#### -- port on which run')
        print('\n\t\tExample:')
        print('\t\t\tbootstrap 25252\n')
        print('\tregural -- regular mode')
        print('\t\t#### -- port on which bootstrap runs')
        print('\t\t$$$$ -- host name of the bootstrap')
        print('\t\t#### -- port on which regular nodes accepts connections')
        print('\n\t\tExample:')
        print('\t\t\tregular 25252 vagrant 36363\n')
