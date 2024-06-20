
class SocketUtility:
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