import sys
#from .dal.services import block_service, hash_service
#from .dal.objects import block, transaction
#from .hashing import crypt_hashing
#from .logger import crypt_logger
from .node import bootstrap, node
#from .p2p import p2p_server, p2p_client, p2p_peer, connection_manager

def start_as_a_bootstrap(bootstrap_port):
    print('\t\tStarting as a bootstrap node at port {}'.format(bootstrap_port))
    bootstrap_node = bootstrap.BootstrapNode(port=bootstrap_port)
    bootstrap_node.accept(True)
    while True:
        user_input = input('\t\t\tEnter a command: ')
        if user_input == 'quit':
            break
    bootstrap_node.close()

def start_as_regular(bootstrap_port, bootstrap_host, node_port, peer_timeout=60, recv_data_size=2048, \
        socket_timeout=10):
    print('\t\tStarting as a regular node')
    a_node = node.Node(node_port)
    a_node.join_network(bootstrap_host, bootstrap_port, peer_timeout=peer_timeout, recv_data_size=recv_data_size, \
            socket_timeout=socket_timeout, read_callback=None)
    a_node.make_silent(True)
    while True:
        user_input = input('\t\t\tEnter a command: ')
        if user_input == 'quit':
            break
        elif user_input == 'msg':
            msg_input = input('\t\t\tEnter a msg to send: ')
            if msg_input != '':
                a_node.connection_manager.send_msg(msg=msg_input)
    a_node.close()

if __name__ == '__main__':
    arguments = sys.argv[1:]
    print('\tThis is CryptoTulips Package')
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
    print('\tEnd of the CryptoTulips Package')
