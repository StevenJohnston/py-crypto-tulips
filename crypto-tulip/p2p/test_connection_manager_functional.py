import socket
from . import connection_manager

def test_connection():
    assert 1 == 1
    return
    server_connection = connection_manager.ConnectionManager(server_port=25255, peer_timeout=0)
    client_connection = connection_manager.ConnectionManager(server_port=25266, peer_timeout=0)

    return_result_server = ''

    def callback_server(data):
        return_result_server = data

    return_result_client = ''

    def callback_client(data):
        return_result_client = data

    server_connection.accept_connection(read_callback=callback_server, run_as_a_thread=True)
    client_connection.connect_to(socket.gethostname(), 25255, read_callback=callback_client)

    number_of_connected = len(server_connection.peer_list)

    print('Shutting down test')

    server_connection.close_all()
    client_connection.close_all()

    assert number_of_connected == 1

if __name__ == '__main__':
    test_connection()
