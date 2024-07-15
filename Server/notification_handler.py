import json
import datetime
class NotificationHandler:
    def __init__(self, db_handler):
        self.db_handler= db_handler

    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/send-notification":
            self.send_notification(client_socket, request)
        elif endpoint == "/get-notification":
            self.get_notification(client_socket)  

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
      