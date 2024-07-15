from database_handler import DatabaseHandler
import json

class UpdateUser:
    def __init__(self, db_handler):
        self.db_handler = db_handler
    
    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/update-user-profile":
            self.update_user_profile(client_socket, request)   

    def update_user_profile(self, client_socket, request):
        role_name = request.get("RoleName")
        user_id = request.get("UserId")
        new_dietpreference = request.get("DietPreference")
        new_spicelevel = request.get("SpiceLevel")
        new_cuisinepreference = request.get("CuisinePreference")
        new_sweettooth = request.get("SweetTooth")
        print(request)
        if role_name == "Employee":
            response = self.db_handler.update_userprofile(user_id, new_dietpreference, new_spicelevel, new_cuisinepreference, new_sweettooth)
            if "success" in response:
                response = {"status": "success", "message": "Profile successfully Updated"}
            else:
                response = {"status": "failure", "message": "There is an error"}
            client_socket.sendall(json.dumps(response).encode()) 