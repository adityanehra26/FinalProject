import json
class FoodMenuHandler:
    def __init__(self, db_handler):
        self.db_handler= db_handler

    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/food_menu":
            self.view_food_menu(client_socket, request)
        elif endpoint == "/delete-menu-item":
            self.delete_menu_item(client_socket, request)
        elif endpoint == "/add-menu-item":
            self.add_menu_item(client_socket, request)
        elif endpoint == "/update-menu-item":
            self.update_menu_item(client_socket, request)
        elif endpoint == "/update-availability":
                self.update_availability(client_socket, request)
        elif endpoint == "/view-low-rating-items":
                self.view_low_rating_items(client_socket, request) 
       
    def add_menu_item(self, client_socket, request):
        role_name = request.get("RoleName")
        if role_name == "Admin":
            response = self.db_handler.add_menuItem(request)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully added"}
            else:
                response = {"status": "failure", "message": "There is an error"}
            client_socket.sendall(json.dumps(response).encode())

    def update_menu_item(self, client_socket, request):
        role_name = request.get("RoleName")
        menuitemid = request.get("MenuItemID")
        new_price = request.get("Price")
        new_availability = request.get("AvailabilityStatus")
        if role_name == "Admin":
            response = self.db_handler.update_menuItem(menuitemid, new_price, new_availability)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully Updated"}
            else:
                response = {"status": "failure", "message": "There is an error"}
            client_socket.sendall(json.dumps(response).encode())       

    def delete_menu_item(self, client_socket, request):
        role_name = request.get("RoleName")
        menuitemid = request.get("MenuItemID")
        if role_name == "Admin":
            response = self.db_handler.delete_menuItem(menuitemid)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully Deleted"}
            else:
                response = {"status": "failure", "message": "There is an error"}
            client_socket.sendall(json.dumps(response).encode())

    def view_food_menu(self, client_socket, request):
        role_name = request.get("role_name")
        if role_name in ["Admin", "Chef","Employee"]:
            menu = self.db_handler.get_food_menu()
            response = {"status": "success", "menu": menu}
        else:
            response = {"status": "failure", "message": "Access denied"}
        client_socket.sendall(json.dumps(response).encode())

    def update_availability(self, client_socket, request):
        role_name = request.get("RoleName")
        menuitemid = request.get("MenuItemID")
        new_availability = request.get("AvailabilityStatus")
        print(request)
        if role_name == "Chef":
            response = self.db_handler.update_menuItemavailabilty(menuitemid, new_availability)
            if "success" in response:
                response = {"status": "success", "message": "Item successfully Updated"}
            else:
                response = {"status": "failure", "message": "There is an error"}
            client_socket.sendall(json.dumps(response).encode())
            
    def view_low_rating_items(self, client_socket, request):
        role_name = request.get("role_name")
        if role_name in ["Admin", "Chef"]:
            low_rating_items = self.db_handler.get_low_rating_items()
            response = {"status": "success", "low_rating_items": low_rating_items}
        else:
            response = {"status": "failure", "message": "Access denied"}
        client_socket.sendall(json.dumps(response).encode())   
    