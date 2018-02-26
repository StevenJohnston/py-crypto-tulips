import socket
import time
from . import bootstrap, node

class CallbackStore():
    return_result_server = ''
    return_result_client = ''
    return_result_second_client = ''
    port_for_server = 23300
    port_for_client = 23400

    @staticmethod
    def clean():
        CallbackStore.return_result_client = ''
        CallbackStore.return_result_server = ''

    @staticmethod
    def increment_ports():
        CallbackStore.port_for_client += 1
        CallbackStore.port_for_server += 1


def callback_client(data):
    CallbackStore.return_result_client = data

def callback_server(data):
    CallbackStore.return_result_server = data

def callback_second_client(data):
    CallbackStore.return_result_second_client = data

def set_up_bootstrap(port_bootstrap):
    boot_node = bootstrap.BootstrapNode(port_bootstrap)
    return boot_node

def test_node_bootstrap_connection():
    port_node = 25266
    port_second_node = 25277
    port_bootstrap = 25255
    boot_node = set_up_bootstrap(port_bootstrap)
    boot_node.accept(True)

    a_node = node.Node(port_node)
    a_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, read_callback=callback_client)

    time.sleep(2)
    second_node = node.Node(port_second_node)
    second_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, read_callback=callback_second_client)

    time.sleep(2)
    first_node_peers = len(a_node.peer_list)
    second_node_peers = len(second_node.peer_list)
    boot_peers = len(boot_node.peer_list)

    a_node.close()
    second_node.close()
    boot_node.close()

    # right now connections node made from
    # bootstrap and internal connections
    # that node accepted are not synced
    assert first_node_peers == 0
    assert second_node_peers == 1
    assert boot_peers == 2


def test_node_bootstrap_send_msg():
    CallbackStore.clean()
    port_node = 25266
    port_second_node = 25277
    port_bootstrap = 25255
    boot_node = set_up_bootstrap(port_bootstrap)
    boot_node.accept(True)

    a_node = node.Node(port_node)
    a_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, read_callback=callback_client)

    time.sleep(2)
    second_node = node.Node(port_second_node)
    second_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, read_callback=callback_second_client)

    time.sleep(5)
    a_node.connection_manager.send_msg('test data1')
    time.sleep(1)
    second_node.connection_manager.send_msg('test data2')
    time.sleep(2)

    a_node.close()
    second_node.close()
    boot_node.close()

    assert CallbackStore.return_result_client == 'test data2'
    assert CallbackStore.return_result_second_client == 'test data1'
