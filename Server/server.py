import socket
import threading
import json
from database_handler import DatabaseHandler
from login_handler import LoginHandler
from recomendation import Recommendation
from food_menu_handler import FoodMenuHandler
from feedback_handler import FeedbackHandler
from voting_handler import VotingHandler
from moms_recipe_handler import MomsrecipeHandler
from notification_handler import NotificationHandler
from rollout_menu import RollOut 
from update_user_profile import UpdateUser

class Server:
    def __init__(self, host, port, db_host, db_user, db_password, db_name):
        self.host = host
        self.port = port
        self.db_handler = DatabaseHandler(db_host, db_user, db_password, db_name)
        self.login_handler = LoginHandler(self.db_handler)
        self.recomendation_engine = Recommendation(self.db_handler)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.food_menu_handler = FoodMenuHandler(self.db_handler) 
        self.feedback_handler = FeedbackHandler(self.db_handler)
        self.voting_handler = VotingHandler(self.db_handler)
        self.notification_handler = NotificationHandler(self.db_handler)
        self.moms_recipe_handler = MomsrecipeHandler(self.db_handler)
        self.rollout_menu = RollOut(self.db_handler)
        self.update_user = UpdateUser(self.db_handler)
        
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
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                raise ValueError("No data received")
            request = json.loads(data)
            print("\n",request)
            endpoint = request.get("endpoint")
            food_menu_endpoints = ["/food_menu", "/delete-menu-item", "/add-menu-item", "/update-menu-item", "/update-availability", "/view-low-rating-items"]
            feedback_endpoints = ["/view-feedback", "/give-feedback"]
            voting_endpoints = ["/voting-items", "/voting"] 
            recommendation_endpoints = ["/view-recomendation"]
            notification_endpoints = ["/send-notification", "/get-notification"]
            moms_recipe_endpoints =["/add-moms-recipe","/view-moms-recipe"]
            rollout_endpoints = ["/roll-out"]
            userupdate_endpoints = ["/update-user-profile"]
            if endpoint == "/login":
                self.login_handler.login(request, client_socket)
            elif endpoint in food_menu_endpoints:
                self.food_menu_handler.endpointHandler(client_socket, request)
            elif endpoint in feedback_endpoints:
                self.feedback_handler.endpointHandler(client_socket, request)
            elif endpoint in voting_endpoints:
                self.voting_handler.endpointHandler(client_socket, request)
            elif endpoint in moms_recipe_endpoints:
                self.moms_recipe_handler.endpointHandler(client_socket, request)
            elif endpoint in recommendation_endpoints:
                self.recomendation_engine.endpointHandler(client_socket, request)
            elif endpoint in notification_endpoints:
                self.notification_handler.endpointHandler(client_socket, request)
            elif endpoint in rollout_endpoints:
                self.rollout_menu.endpointHandler(client_socket, request)            
            elif endpoint in userupdate_endpoints:
                self.update_user.endpointHandler(client_socket, request)   
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
        
            
if __name__ == "__main__":
    server = Server('localhost', 12345, 'localhost', 'root', '12345678', 'cafeteria')
    server.start_server()
