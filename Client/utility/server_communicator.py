import socket
import json

class ServerCommunicator:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def connect_to_server(self, host, port):
        self.client_socket.connect((host, port))
        
    def send_to_server(self, msg):
        self.client_socket.sendall(msg)

    def receive_msg_from_server(self):
        return self.client_socket.recv(1024).decode()
    
    def close_connection(self):
        self.client_socket.close()
    
    def send_request(self, endpoint, data=None):
        request = {"endpoint": endpoint}
        if data:
            request.update(data)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.sendall(json.dumps(request).encode())

        buffer_size = 4096
        response = ""
        while True:
            part = client_socket.recv(buffer_size).decode()
            response += part
            if len(part) < buffer_size:
                break

        client_socket.close()
        return json.loads(response)