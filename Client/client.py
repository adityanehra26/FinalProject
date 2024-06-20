import socket
import json
from userHandler.chef import Chef
from userHandler.admin import Admin
from userHandler.employee import Employee
from utility.socket_functions import SocketUtility

def login(username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_utility = SocketUtility(client_socket)

    request = {
        "endpoint": "/login",
        "username": username,
        "password": password
    }
    
    socket_utility.connect_to_server('localhost', 12345)
    json_data = json.dumps(request).encode()
    socket_utility.send_to_server(json_data)
    response = socket_utility.receive_msg_from_server()
    response = json.loads(response)
    response = response['user']
    print(response)
    if(response['RoleName'] == "Admin"):
        user = Admin(response['ID'], response['Name'], response['RoleName'], socket_utility)
        user.user_menu()
    elif(response['RoleName'] == "Chef"):
        user = Chef(response['ID'], response['Name'], response['RoleName'], socket_utility)
        user.user_menu()
    elif(response['RoleName'] == "Employee"):
        user = Employee(response['ID'], response['Name'], response['RoleName'], socket_utility)
        user.user_menu()
    else:
        print("\nInvalid Creds")   

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = login(username, password)
    print(response)
