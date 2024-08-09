import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
from login_handler import LoginHandler
from database_handler import DatabaseHandler
import json

class TestLoginHandler(unittest.TestCase):

    @patch.object(DatabaseHandler, 'check_login')
    def test_login_admin_success(self, mock_check_login):
        mock_check_login.return_value = {
            "ID": 1,
            "Name": "admin",
            "RoleName": "Admin"
        }

        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        login_handler = LoginHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "username": "admin",
            "password": "admin"
        }

        login_handler.login(request, client_socket)

        expected_response = {
            "status": "success",
            "user": {
                "ID": 1,
                "Name": "admin",
                "RoleName": "Admin"
            }
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())

    @patch.object(DatabaseHandler, 'check_login')
    def test_login_chef_success(self, mock_check_login):
        mock_check_login.return_value = {
            "ID": 2,
            "Name": "chef",
            "RoleName": "Chef"
        }

        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        login_handler = LoginHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "username": "chef",
            "password": "chef"
        }

        login_handler.login(request, client_socket)

        expected_response = {
            "status": "success",
            "user": {
                "ID": 2,
                "Name": "chef",
                "RoleName": "Chef"
            }
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())

    @patch.object(DatabaseHandler, 'check_login')
    def test_login_employee_success(self, mock_check_login):
        mock_check_login.return_value = {
            "ID": 3,
            "Name": "user3",
            "RoleName": "Employee"
        }

        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        login_handler = LoginHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "username": "user3",
            "password": "user3"
        }

        login_handler.login(request, client_socket)

        expected_response = {
            "status": "success",
            "user": {
                "ID": 3,
                "Name": "user3",
                "RoleName": "Employee"
            }
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())

    @patch.object(DatabaseHandler, 'check_login')
    def test_login_failure(self, mock_check_login):
        mock_check_login.return_value = None

        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        login_handler = LoginHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "username": "nonexistent_user",
            "password": "wrong_password"
        }

        login_handler.login(request, client_socket)
        expected_response = {
            "status": "falure",
            "message": "Invalid credentials"
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())

if __name__ == "__main__":
    unittest.main()
