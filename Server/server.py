import socket
import threading
import json
from database_handler import DatabaseHandler
from login_handler import LoginHandler
from recomendation import Recommendation

class Server:
    def __init__(self, host, port, db_host, db_user, db_password, db_name):
        self.host = host
        self.port = port
        self.db_handler = DatabaseHandler(db_host, db_user, db_password, db_name)
        self.login_handler = LoginHandler(self.db_handler)
        self.recomendation_engine = Recommendation(self.db_handler)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.db_handler.connect()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            request = json.loads(data)
            endpoint = request.get("endpoint")
            if endpoint == "/login":
                self.login_handler.login(request, client_socket)
            elif endpoint == "/food_menu":
                self.view_food_menu(client_socket, request)
            elif endpoint == "/delete-menu-item":
                self.delete_menu_item(client_socket, request)
            elif endpoint == "/add-menu-item":
                print(request)
                self.add_menu_item(client_socket, request)
            elif endpoint == "/update-menu-item":
                self.update_menu_item(client_socket, request)
            elif endpoint == "/roll-out-menu":
                self.roll_out_menu(client_socket, request)
            elif endpoint == "/view-recomendation":
                self.view_recomendation(client_socket, request)
            else:
                response = {"status": "failure", "message": "Invalid endpoint"}
                client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def roll_out_menu(self):
        pass
    
    def view_recomendation(self, client_socket, request):
        role_name = request.get("RoleName")
        print(request, role_name)
        if role_name == "Chef":
            response = self.recomendation_engine.recommend_food_items()
            print(response)
            response = {"status": "success", "recomendations": response}
            client_socket.sendall(json.dumps(response).encode())

    def update_menu_item(self, client_socket, request):
        print(request)
        role_name = request.get("RoleName")
        menuitemid = request.get("MenuItemID")
        new_price = request.get("Price")
        new_availability = request.get("AvailabilityStatus")
        print(role_name, menuitemid, new_availability, new_price)
        if role_name == "Admin":
            response = self.db_handler.update_menuItem(menuitemid, new_price, new_availability)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully Updated"}
            else:
                response = {"status": "success", "message": "There is error"}
            client_socket.sendall(json.dumps(response).encode())

    def add_menu_item(self, client_socket, request):
        print(request)
        role_name = request.get("RoleName")
        print(f"Inside add food item {role_name} {request}")
        if role_name == "Admin":
            print("Inside role")
            response = self.db_handler.add_menuItem(request)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully added"}
            else:
                response = {"status": "success", "message": "There is error"}
            client_socket.sendall(json.dumps(response).encode())

    def delete_menu_item(self, client_socket, request):
        role_name = request.get("RoleName")
        menuitemid = request.get("MenuItemID")
        if role_name == "Admin":
            response = self.db_handler.delete_menuItem(menuitemid)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully Deleted"}
            else:
                response = {"status": "success", "message": "There is error"}
            client_socket.sendall(json.dumps(response).encode())

    def view_food_menu(self, client_socket, request):
        role_name = request.get("role_name")
        if role_name in ["Admin", "Chef"]:
            menu = self.db_handler.get_food_menu()
            response = {"status": "success", "menu": menu}
        else:
            response = {"status": "failure", "message": "Access denied"}
        client_socket.sendall(json.dumps(response).encode())

if __name__ == "__main__":
    server = Server('localhost', 12345, 'localhost', 'root', '12345678', 'cafeteria')
    server.start_server()
