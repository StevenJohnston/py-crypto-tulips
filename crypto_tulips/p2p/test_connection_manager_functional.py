import socket
import time
from . import connection_manager

def set_up_server_client(server_port, client_port, peer_timeout=0, socket_timeout=0.1):
    server_connection = connection_manager.ConnectionManager(server_port=server_port, peer_timeout=peer_timeout, socket_timeout=socket_timeout)
    client_connection = connection_manager.ConnectionManager(server_port=client_port, peer_timeout=peer_timeout, socket_timeout=socket_timeout)
    return server_connection, client_connection

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


def test_connection():
    CallbackStore.clean()
    server_port = CallbackStore.port_for_server
    client_port = CallbackStore.port_for_client
    CallbackStore.increment_ports()

    server_connection, client_connection = set_up_server_client(server_port, client_port)

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)

    number_of_connected_server = len(server_connection.peer_list)
    number_of_connected_client = len(client_connection.peer_list)

    client_connection.close_all()
    time.sleep(0.1)
    server_connection.close_all()

    assert number_of_connected_server == 1
    assert number_of_connected_client == 1

def test_client_send():
    CallbackStore.clean()
    server_port = CallbackStore.port_for_server
    client_port = CallbackStore.port_for_client
    CallbackStore.increment_ports()

    server_connection, client_connection = set_up_server_client(server_port, client_port)

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)

    client_connection.send_msg('test data')
    time.sleep(0.1)

    client_connection.close_all()
    server_connection.close_all()

    assert CallbackStore.return_result_server == 'test data'
    assert CallbackStore.return_result_client == ''

def test_server_send():
    CallbackStore.clean()
    server_port = CallbackStore.port_for_server
    client_port = CallbackStore.port_for_client
    CallbackStore.increment_ports()

    server_connection, client_connection = set_up_server_client(server_port, client_port)

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)

    server_connection.send_msg('test data')
    time.sleep(0.1)

    client_connection.close_all()
    server_connection.close_all()

    assert CallbackStore.return_result_client == 'test data'
    assert CallbackStore.return_result_server == ''

def test_multiple_client_send():
    CallbackStore.clean()
    server_port = CallbackStore.port_for_server
    client_port = CallbackStore.port_for_client
    CallbackStore.increment_ports()

    server_connection, client_connection = set_up_server_client(server_port, client_port)
    second_client = connection_manager.ConnectionManager(server_port=22222, peer_timeout=0, socket_timeout=0.1)

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_second_client)

    server_connection.send_msg('test data')
    time.sleep(0.1)

    client_connection.close_all()
    second_client.close_all()
    server_connection.close_all()

    assert CallbackStore.return_result_client == 'test data'
    assert CallbackStore.return_result_server == ''
    assert CallbackStore.return_result_second_client == 'test data'

def test_peer_timeout():
    CallbackStore.clean()
    server_port = CallbackStore.port_for_server
    client_port = CallbackStore.port_for_client
    CallbackStore.increment_ports()

    server_connection = connection_manager.ConnectionManager(server_port=server_port, peer_timeout=0.5, socket_timeout=0.1)
    client_connection = connection_manager.ConnectionManager(server_port=client_port, peer_timeout=0, socket_timeout=0.1)
    second_client = connection_manager.ConnectionManager(server_port=22322, peer_timeout=0, socket_timeout=1)

    time.sleep(0.1)
    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)
    time.sleep(1.5)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_second_client)

    server_connection.send_msg('test data')
    time.sleep(0.1)

    client_connection.close_all()
    second_client.close_all()
    server_connection.close_all()

    assert CallbackStore.return_result_server == ''
    assert CallbackStore.return_result_client == ''
    assert CallbackStore.return_result_second_client == 'test data'

if __name__ == '__main__':
    test_connection()
    print('*'*100)
    test_client_send()
    print('*'*100)
    test_server_send()
    print('*'*100)
    test_multiple_client_send()
    print('*'*100)
    test_peer_timeout()
