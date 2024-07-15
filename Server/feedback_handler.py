import json
class FeedbackHandler:
    def __init__(self, db_handler):
        self.db_handler= db_handler

    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/view-feedback":
            self.view_feedback(client_socket, request)
        elif endpoint == "/give-feedback":
            self.give_feedback(client_socket, request)

    def view_feedback(self, client_socket, request):
        role_name = request.get("role_name")
        feedback = self.db_handler.get_feedback_details()
        print(feedback)
        response = {"status": "success", "feedback": feedback}
        client_socket.sendall(json.dumps(response).encode())

    def give_feedback(self, client_socket, request):
        role_name = request.get("RoleName")
        if role_name == "Employee":
            response = self.db_handler.give_menuItemfeedback(request)
            if "success" in response:
                response = {"status": "success", "message": "Successfully given feedback"}
            else:
                response = {"status": "failure", "message": "There is an error"}
        else:
            response = {"status": "failure", "message": "Invalid role for giving feedback"}

        client_socket.sendall(json.dumps(response).encode())  
      