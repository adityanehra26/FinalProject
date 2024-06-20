import json

class LoginHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def login(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            request = json.loads(data)
            if request.get("endpoint") == "/login":
                username = request["username"]
                password = request["password"]
                user = self.db_handler.check_login(username, password)
                if user:
                    response = {
                        "status": "success",
                        "user": {
                            "ID": user["ID"],
                            "Name": user["Name"],
                            "RoleName": user["RoleName"]
                        }
                    }
                else:
                    response = {"status": "failure", "message": "Invalid credentials"}
                client_socket.sendall(json.dumps(response).encode())
            else:
                response = {"status": "failure", "message": "Invalid endpoint"}
                client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
