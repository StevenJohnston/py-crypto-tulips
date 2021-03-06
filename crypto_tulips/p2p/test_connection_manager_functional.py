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
    return_peer_id_server = ''
    return_peer_id_client = ''
    return_peer_id_second_client = ''
    port_for_server = 23300
    port_for_client = 23400

    @staticmethod
    def clean():
        CallbackStore.return_result_client = ''
        CallbackStore.return_result_server = ''
        CallbackStore.return_result_second_client = ''
        CallbackStore.return_peer_id_client = ''
        CallbackStore.return_peer_id_server = ''
        CallbackStore.return_peer_id_second_client = ''

    @staticmethod
    def increment_ports():
        CallbackStore.port_for_client += 1
        CallbackStore.port_for_server += 1


def callback_client(data, peer_id):
    CallbackStore.return_result_client = data
    CallbackStore.return_peer_id_client = peer_id

def callback_server(data, peer_id):
    CallbackStore.return_result_server = data
    CallbackStore.return_peer_id_server = peer_id

def callback_second_client(data, peer_id):
    CallbackStore.return_result_second_client = data
    CallbackStore.return_peer_id_second_client = peer_id


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
    server_connection.need_to_check_for_duplicate = False
    client_connection.need_to_check_for_duplicate = False
    second_client = connection_manager.ConnectionManager(server_port=22222, peer_timeout=0, socket_timeout=0.1)
    second_client.need_to_check_for_duplicate = False

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)
    second_client.connect_to(socket.gethostname(), server_port, read_callback=callback_second_client)

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
    server_connection.need_to_check_for_duplicate = False
    client_connection = connection_manager.ConnectionManager(server_port=client_port, peer_timeout=0, socket_timeout=0.1)
    client_connection.need_to_check_for_duplicate = False
    second_client = connection_manager.ConnectionManager(server_port=22322, peer_timeout=0, socket_timeout=1)
    second_client.need_to_check_for_duplicate = False

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

def test_peer_id():
    CallbackStore.clean()
    server_port = CallbackStore.port_for_server
    client_port = CallbackStore.port_for_client
    CallbackStore.increment_ports()

    server_connection, client_connection = set_up_server_client(server_port, client_port)
    server_connection.need_to_check_for_duplicate = False
    client_connection.need_to_check_for_duplicate = False
    second_client = connection_manager.ConnectionManager(server_port=22222, peer_timeout=0, socket_timeout=0.1)
    second_client.need_to_check_for_duplicate = False

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)
    second_client.connect_to(socket.gethostname(), server_port, read_callback=callback_second_client)

    server_connection.send_msg('test data')
    time.sleep(0.1)
    first_peer_id_cliet = CallbackStore.return_peer_id_client
    first_peer_id_second_client = CallbackStore.return_peer_id_second_client
    time.sleep(0.1)
    server_connection.send_msg('second data')
    time.sleep(0.1)
    second_peer_id_client = CallbackStore.return_peer_id_client
    second_peer_id_second_client = CallbackStore.return_peer_id_second_client

    client_connection.close_all()
    second_client.close_all()
    server_connection.close_all()

    assert first_peer_id_cliet == second_peer_id_client and first_peer_id_cliet is not None
    assert first_peer_id_second_client == second_peer_id_second_client and first_peer_id_second_client is not None

def test_peer_send_one():
    CallbackStore.clean()
    server_port = CallbackStore.port_for_server
    client_port = CallbackStore.port_for_client
    CallbackStore.increment_ports()

    server_connection, client_connection = set_up_server_client(server_port, client_port)
    server_connection.need_to_check_for_duplicate = False
    client_connection.need_to_check_for_duplicate = False
    second_client = connection_manager.ConnectionManager(server_port=22222, peer_timeout=0, socket_timeout=0.1)
    second_client.need_to_check_for_duplicate = False

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), server_port, read_callback=callback_client)
    second_client.connect_to(socket.gethostname(), server_port, read_callback=callback_second_client)

    server_connection.send_msg('test data')
    time.sleep(0.1)
    first_peer_id_cliet = CallbackStore.return_peer_id_client
    first_peer_id_second_client = CallbackStore.return_peer_id_second_client
    time.sleep(0.1)
    CallbackStore.return_result_second_client = ''
    CallbackStore.return_result_client = ''
    CallbackStore.return_result_server = ''
    client_connection.send_msg('test data', target_peer_id=first_peer_id_cliet)
    time.sleep(0.1)
    first_result_server = CallbackStore.return_result_server
    first_result_second_client = CallbackStore.return_result_second_client
    first_result_client = CallbackStore.return_result_client
    CallbackStore.return_result_second_client = ''
    CallbackStore.return_result_client = ''
    CallbackStore.return_result_server = ''
    second_client.send_msg('test data2', target_peer_id=first_peer_id_second_client)
    time.sleep(0.1)
    second_result_server = CallbackStore.return_result_server
    second_result_client = CallbackStore.return_result_client
    second_result_second_client = CallbackStore.return_result_second_client

    client_connection.close_all()
    second_client.close_all()
    server_connection.close_all()

    assert first_peer_id_cliet is not None and first_peer_id_cliet != ''
    assert first_peer_id_second_client is not None and first_peer_id_second_client != ''

    assert first_result_server == 'test data'
    assert first_result_second_client == ''
    assert first_result_client == ''
    assert second_result_server == 'test data2'
    assert second_result_client == ''
    assert second_result_second_client == ''
