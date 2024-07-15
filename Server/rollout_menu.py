from database_handler import DatabaseHandler
import json

class RollOut:
    def __init__(self, db_handler):
        self.db_handler = db_handler
    
    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/roll-out":
            self.roll_out_menu(client_socket,request) 

    def roll_out_menu(self, client_socket, request):
        data = request.get("data")
       
        truncate_result = self.db_handler.truncate_recommended_menu_item_table()
        if truncate_result == "failure":
            response = {"status": "failure", "message": "Failed to truncate recommendedmenuitem table"}
            client_socket.sendall(json.dumps(response).encode())
            return
        self.db_handler.reset_form_filled_status_for_all_user()
        results = []
        try:
            for meal, menu_items in data.items():
                for item in menu_items:
                    menu_item_id = int(item)
                    result = self.db_handler.add_recommended_menu_item(menu_item_id, 0)  # Initial votes set to 0
                    results.append(result)
            if all(result == "success" for result in results):
                self.db_handler.send_notification("Tomorrow's Menu Rolled Out, Fill your choice(If not).")
                response = {"status": "success", "message": "Menu items are rolled out successfully"}
            else:
                response = {"status": "failure", "message": "An error occurred while adding menu items"}
        except Exception as e:
            print(f"Error in roll_out_menu: {e}")
            response = {"status": "failure", "message": "An error occurred while adding menu items"}
        client_socket.sendall(json.dumps(response).encode())
