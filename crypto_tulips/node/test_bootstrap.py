import socket
import time
from . import bootstrap, node

def test_bootstrap_accept():
    port_bootstrap = 25255
    port_node = 25266
    port_second_node = 25277
    peer_timeout = 0
    socket_timeout = 0.1
    boot_node = bootstrap.BootstrapNode(port_bootstrap)
    boot_node.accept(True)
    a_node = node.Node(port_node)
    a_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, peer_timeout=peer_timeout, socket_timeout=socket_timeout)
    time.sleep(0.1)
    second_node = node.Node(port_second_node)
    second_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, peer_timeout=peer_timeout, socket_timeout=socket_timeout)
    time.sleep(0.1)
    number_of_connections = len(boot_node.peer_list)
    second_node.close()
    a_node.close()
    boot_node.close()
    assert number_of_connections == 2

def test_bootstrap_accept_duplicate():
    port_bootstrap = 25255
    port_node = 25266
    peer_timeout = 0
    socket_timeout = 0.1
    boot_node = bootstrap.BootstrapNode(port_bootstrap)
    boot_node.accept(True)
    a_node = node.Node(port_node)
    a_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, peer_timeout=peer_timeout, socket_timeout=socket_timeout)
    time.sleep(0.1)
    a_node.close()
    time.sleep(0.1)
    a_node.join_network(bootstrap_host=socket.gethostname(), \
            bootstrap_port=port_bootstrap, peer_timeout=peer_timeout, socket_timeout=socket_timeout)
    time.sleep(0.1)
    number_of_connections = len(boot_node.peer_list)
    a_node.close()
    boot_node.close()
    assert number_of_connections == 1
