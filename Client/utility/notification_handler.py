class NotificationHandler:
    def __init__(self, server_communicator):
        self.server_communicator = server_communicator
    
    def get_notification(self):
        endpoint = "/get-notification"
        response = self.server_communicator.send_request(endpoint)
        response = response["notifications"]
        return response
    

    def send_notification(self, message):
        endpoint = "send-notification"
        response = self.server_communicator.send_request(endpoint, message)
        if response["status"] == "success":
            return "Notification is send successfully" 
        else:
            return "Not able to send the notification"