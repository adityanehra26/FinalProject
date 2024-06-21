import socket
import threading
import json
from database_handler import DatabaseHandler
from login_handler import LoginHandler
from recomendation import Recomendation

class Server:
    def __init__(self, host, port, db_host, db_user, db_password, db_name):
        self.host = host
        self.port = port
        self.db_handler = DatabaseHandler(db_host, db_user, db_password, db_name)
        self.login_handler = LoginHandler(self.db_handler)
        self.recomendation_engine = Recomendation(self.db_handler)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.db_handler.connect()
        if not self.db_handler.conn:
            print("Failed to connect to the database. Exiting...")
            return
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
            if not data:
                raise ValueError("No data received")
            request = json.loads(data)
            print("Request : ",request)
            endpoint = request.get("endpoint")
            if endpoint == "/login":
                self.login_handler.login(request, client_socket)
            elif endpoint == "/food_menu":
                self.view_food_menu(client_socket, request)
            elif endpoint == "/delete-menu-item":
                self.delete_menu_item(client_socket, request)
            elif endpoint == "/add-menu-item":
                self.add_menu_item(client_socket, request)
            elif endpoint == "/update-menu-item":
                self.update_menu_item(client_socket, request)
            elif endpoint == "/view-recomendation":
                self.view_recomendation(client_socket, request)
            elif endpoint == "/view-feedback":
                self.view_feedback(client_socket, request)
            else:
                response = {"status": "failure", "message": "Invalid endpoint"}
                client_socket.sendall(json.dumps(response).encode())
        except ValueError as ve:
            print(f"ValueError: {ve}")
            response = {"status": "failure", "message": "Invalid request format or no data received"}
            client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
            response = {"status": "failure", "message": "An error occurred"}
            client_socket.sendall(json.dumps(response).encode())
        finally:
            client_socket.close()

    def roll_out_menu(self, client_socket, request):
        pass
    
    def view_recomendation(self, client_socket, request):
        role_name = request.get("RoleName")
        if role_name == "Chef":
            response = self.recomendation_engine.recommend_food_items()
            response = {"status": "success", "recomendations": response}
            client_socket.sendall(json.dumps(response).encode())
    
    def view_feedback(self, client_socket, request):
        role_name = request.get("role_name")
        print("Inside chef",request)
        feedback = self.db_handler.get_feedback_details()
        print(feedback)
        response = {"status": "success", "feedback": feedback}
        client_socket.sendall(json.dumps(response).encode())

    def update_menu_item(self, client_socket, request):
        role_name = request.get("RoleName")
        menuitemid = request.get("MenuItemID")
        new_price = request.get("Price")
        new_availability = request.get("AvailabilityStatus")
        if role_name == "Admin":
            response = self.db_handler.update_menuItem(menuitemid, new_price, new_availability)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully Updated"}
            else:
                response = {"status": "failure", "message": "There is an error"}
            client_socket.sendall(json.dumps(response).encode())

    def add_menu_item(self, client_socket, request):
        role_name = request.get("RoleName")
        if role_name == "Admin":
            response = self.db_handler.add_menuItem(request)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully added"}
            else:
                response = {"status": "failure", "message": "There is an error"}
            client_socket.sendall(json.dumps(response).encode())

    def delete_menu_item(self, client_socket, request):
        role_name = request.get("RoleName")
        menuitemid = request.get("MenuItemID")
        if role_name == "Admin":
            response = self.db_handler.delete_menuItem(menuitemid)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully Deleted"}
            else:
                response = {"status": "failure", "message": "There is an error"}
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
