import socket
import json
from userHandler.chef import Chef
from userHandler.admin import Admin
from userHandler.employee import Employee
from utility.server_communicator import ServerCommunicator


def login(username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_communicator = ServerCommunicator(client_socket)

    
    endpoint =  "/login"
    data = {
        "username": username,
        "password": password
    }
    
    server_communicator.connect_to_server('localhost', 12345)
    response = server_communicator.send_request(endpoint, data)

    if(response['status'] != "success"):
        print("Invalid creds!\nExiting...")
        return
    
    response = response['user']
    if(response['RoleName'] == "Admin"):
        user = Admin(response['ID'], response['Name'], response['RoleName'], server_communicator)
        user.user_menu()
    elif(response['RoleName'] == "Chef"):
        user = Chef(response['ID'], response['Name'], response['RoleName'], server_communicator)
        user.user_menu()
    elif(response['RoleName'] == "Employee"):
        user = Employee(response['ID'], response['Name'], response['RoleName'], server_communicator)
        user.user_menu() 




if __name__ == "__main__":
    # Example usage
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_response = login(username, password)
    print(login_response)


