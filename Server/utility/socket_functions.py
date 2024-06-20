
class SocketUtility:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def send_to_client(self, msg):
        self.client_socket.sendall(msg.encode())

    def receive_msg_from_client(self):
        return self.client_socket.recv(1024).decode()
    
    def close_connection(self):
        self.client_socket.close()