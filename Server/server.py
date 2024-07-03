import socket
import threading
import json
from database_handler import DatabaseHandler
from login_handler import LoginHandler
from recomendation import Recomendation
import datetime

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
            elif endpoint == "/roll-out":
                self.roll_out_menu(client_socket, request)
            elif endpoint == "/voting":
                self.vote_for_menu(client_socket, request)
            elif endpoint == "/voting-items":
                self.view_voting_items(client_socket)
            elif endpoint == "/send-notification":
                self.send_notification(client_socket, request)
            elif endpoint == "/get-notification":
                self.get_notification(client_socket)
            else:
                response = {"status": "failure", "message": "Invalid endpoint"}
                client_socket.sendall(json.dumps(response).encode())

        except ValueError as ve:
            print(f"ValueError: {ve}")
            response = {"status": "failure", "message": "Invalid request format or no data received"}
            client_socket.sendall(json.dumps(response).encode())
        except ConnectionResetError:
            print("Connection was forcibly closed by the remote host")
        except Exception as e:
            print(f"Error: {e}")
            response = {"status": "failure", "message": "An error occurred"}
            client_socket.sendall(json.dumps(response).encode())
        finally:
            client_socket.close()

    def send_notification(self, client_socket, request):
        message = request.get("message")
        try:
            self.db_handler.send_notification(message)
            response = {"status": "success", "message": "Notification sent successfully"}
        except Exception as e:
            print(f"Error sending notification: {e}")
            response = {"status": "failure", "message": "Failed to send notification"}
        client_socket.sendall(json.dumps(response).encode())

    def get_notification(self, client_socket):
        try:
            notifications = self.db_handler.get_notification()
            # Convert date objects to string
            notifications = [
                (notification_id, message, date.isoformat() if isinstance(date, datetime.date) else date)
                for notification_id, message, date in notifications
            ]
            response = {"status": "success", "notifications": notifications}
        except Exception as e:
            print(f"Error fetching notifications: {e}")
            response = {"status": "failure", "message": "Failed to fetch notifications"}
        client_socket.sendall(json.dumps(response).encode())

    def roll_out_menu(self, client_socket, request):
        data = request.get("data")
       
        truncate_result = self.db_handler.truncate_recommended_menu_item_table()
        if truncate_result == "failure":
            response = {"status": "failure", "message": "Failed to truncate recommendedmenuitem table"}
            client_socket.sendall(json.dumps(response).encode())
            return
        self.db_handler.reset_form_filled_status_for_all_user()
        results = []
        try:
            for meal, menu_items in data.items():
                for item in menu_items:
                    menu_item_id = int(item)
                    result = self.db_handler.add_recommended_menu_item(menu_item_id, 0)  # Initial votes set to 0
                    results.append(result)
            if all(result == "success" for result in results):
                self.db_handler.send_notification("Tomorrow's Menu Rolled Out, Fill your choice(If not).")
                response = {"status": "success", "message": "Menu items are rolled out successfully"}
            else:
                response = {"status": "failure", "message": "An error occurred while adding menu items"}
        except Exception as e:
            print(f"Error in roll_out_menu: {e}")
            response = {"status": "failure", "message": "An error occurred while adding menu items"}
        client_socket.sendall(json.dumps(response).encode())
    
    def view_recomendation(self, client_socket, request):
        role_name = request.get("RoleName")
        if role_name == "Chef":
            response = self.recomendation_engine.recommend_food_items()
            response = {"status": "success", "recomendations": response}
            client_socket.sendall(json.dumps(response).encode())

    def view_voting_items(self, client_socket):
        try:
            voting_items = self.db_handler.get_voting_items()
            categorized_items = {"Breakfast": [], "Lunch": [], "Dinner": []}

            for item in voting_items:
                meal_type = item[2]
                categorized_items[meal_type].append({
                    "MenuItemID": item[0],
                    "MenuItemName": item[1],
                    "Votes": item[3]
                })

            response = {"status": "success", "data": categorized_items}
            client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error in view_voting_items: {e}")
            response = {"status": "failure", "message": "An error occurred while fetching voting items"}
            client_socket.sendall(json.dumps(response).encode())

    def vote_for_menu(self, client_socket, request):
        employee_id = request.get("employee_id")
        data = request.get("data")
        try:
            form_filled_status = self.db_handler.check_form_filled_status(employee_id)
            print(form_filled_status)
            if form_filled_status == 1:
                response = {"status": "failure", "message": "You already voted"}
            else:
                for meal, menu_item_id in data.items():
                    self.db_handler.add_vote(menu_item_id)
                self.db_handler.update_form_filled_status(employee_id, 1)
                response = {"status": "success", "message": "Votes cast successfully"}
        except Exception as e:
            print(f"Error in vote_for_menu: {e}")
            response = {"status": "failure", "message": "An error occurred while voting"}
        client_socket.sendall(json.dumps(response).encode())

    def give_feedback(self):
        menu_item_id = input("Enter the Menu Item ID: ")
        rating = input("Enter your Rating (e.g., 4.5): ")
        comment = input("Enter your Comment: ")
        endpoint = "/give-feedback"
        data = {
            "UserID": self.user_id,
            "MenuItemID": int(menu_item_id),
            "Rating": float(rating),
            "Comment": comment,
            "RoleName": "Employee"
        }
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    def view_feedback(self, client_socket, request):
        role_name = request.get("role_name")
        print("Inside chef",request)
        feedback = self.db_handler.get_feedback_details()
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
