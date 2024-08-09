import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock, patch
from feedback_handler import FeedbackHandler
from database_handler import DatabaseHandler
import json

class TestFeedbackHandler(unittest.TestCase):

    @patch.object(DatabaseHandler, 'get_feedback_details')
    def test_view_feedback_success(self, mock_get_feedback_details):
        mock_get_feedback_details.return_value = [
            {
                "FeedbackID": 1,
                "UserName": "user3",
                "FoodName": "Aloo Puri",
                "Rating": 1,
                "Comment": "Aloo Puri was bad",
                "Date": "2024-06-20"
            },
            {
                "FeedbackID": 2,
                "UserName": "user4",
                "FoodName": "Aloo Puri",
                "Rating": 3,
                "Comment": "Enjoyed the Aloo Puri!",
                "Date": "2024-06-20"
            }
        ]

        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        feedback_handler = FeedbackHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "endpoint": "/view-feedback",
            "role_name": "Admin"
        }

        feedback_handler.endpointHandler(client_socket, request)

        expected_response = {
            "status": "success",
            "feedback": [
                {
                    "FeedbackID": 1,
                    "UserName": "user3",
                    "FoodName": "Aloo Puri",
                    "Rating": 1,
                    "Comment": "Aloo Puri was bad",
                    "Date": "2024-06-20"
                },
                {
                    "FeedbackID": 2,
                    "UserName": "user4",
                    "FoodName": "Aloo Puri",
                    "Rating": 3,
                    "Comment": "Enjoyed the Aloo Puri!",
                    "Date": "2024-06-20"
                }
            ]
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())
        print("Test: View Feedback Success - Passed")

    @patch.object(DatabaseHandler, 'give_menuItemfeedback')
    def test_give_feedback_success(self, mock_give_menuItemfeedback):
        mock_give_menuItemfeedback.return_value = "success"

        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        feedback_handler = FeedbackHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "endpoint": "/give-feedback",
            "RoleName": "Employee",
            "UserID": 3,
            "MenuItemID": 1,
            "Rating": 4,
            "Comment": "Good"
        }

        feedback_handler.endpointHandler(client_socket, request)

        expected_response = {
            "status": "success",
            "message": "Successfully given feedback"
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())
        print("Test: Give Feedback Success - Passed")

    @patch.object(DatabaseHandler, 'give_menuItemfeedback')
    def test_give_feedback_failure(self, mock_give_menuItemfeedback):
        mock_give_menuItemfeedback.return_value = "error"

        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        feedback_handler = FeedbackHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "endpoint": "/give-feedback",
            "RoleName": "Employee",
            "UserID": 3,
            "MenuItemID": 1,
            "Rating": 4,
            "Comment": "Good"
        }

        feedback_handler.endpointHandler(client_socket, request)

        expected_response = {
            "status": "failure",
            "message": "There is an error"
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())
        print("Test: Give Feedback Failure - Passed")

    def test_give_feedback_invalid_role(self):
        db_handler = DatabaseHandler('localhost', 'root', '12345678', 'cafeteria')
        feedback_handler = FeedbackHandler(db_handler)
        client_socket = MagicMock()

        request = {
            "endpoint": "/give-feedback",
            "RoleName": "Chef",
            "UserID": 3,
            "MenuItemID": 1,
            "Rating": 4,
            "Comment": "Good"
        }

        feedback_handler.endpointHandler(client_socket, request)

        expected_response = {
            "status": "failure",
            "message": "Invalid role for giving feedback"
        }

        client_socket.sendall.assert_called_once_with(json.dumps(expected_response).encode())
        print("Test: Give Feedback Invalid Role - Passed")

if __name__ == "__main__":
    unittest.main()
