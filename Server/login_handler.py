import json

class LoginHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def login(self, request, client_socket):
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
        print(response)
        client_socket.sendall(json.dumps(response).encode())
