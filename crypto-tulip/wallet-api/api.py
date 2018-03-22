from flask import Flask
from flask_restful import Resource, Api
import socket
import ssl
import json
app = Flask(__name__)
api = Api(app)

class Node(Resource):

    def get(self):
        certfile = 'cacert.pem'
        sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        nodeSocket = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, \
               ca_certs=certfile)
        nodeSocket.connect(("192.168.33.10",36363))
        nodeSocket.send('wallet'.encode())
        json_ip_info = self.convert_to_json('get_all_ip', '')
        msg_json = json.dumps(json_ip_info, sort_keys=True)
        nodeSocket.send(msg_json.encode())
        data = nodeSocket.recv(1024).decode()
        print(data)
        json_quit = self.convert_to_json('exit', 'quit')
        msg_json = json.dumps(json_quit, sort_keys=True)
        nodeSocket.send(msg_json.encode())
        nodeSocket.send('quit'.encode())
        return {
            'ipaddress': [
                '192.168.10.2',
                '192.168.10.1'
            ]
        }
    def convert_to_json(self, action, data):
        return {
                "action" : action,
                "data" : data
        }

api.add_resource(Node, '/getAllIP')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)