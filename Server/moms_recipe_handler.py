import json
class MomsrecipeHandler:
    def __init__(self, db_handler):
        self.db_handler= db_handler

    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/add-moms-recipe":
            self.moms_recipe(client_socket,request)   
        elif endpoint == "/view-moms-recipe":
            self.view_moms_recipe(client_socket,request) 

    def moms_recipe(self, client_socket, request):
        user_id = request.get("UserID")
        moms_recipe = request.get("Recipe")
        print(request)
        try:
            response = self.db_handler.add_moms_recipe(user_id, moms_recipe)
            if response == "success":
                response = {"status": "success", "message": "Mom's recipe successfully added"}
            else:
                response = {"status": "failure", "message": "Failed to add Mom's recipe"}
        except Exception as e:
            print(f"Error in moms_recipe: {e}")
            response = {"status": "failure", "message": "An error occurred while adding Mom's recipe"}
        client_socket.sendall(json.dumps(response).encode())

    def view_moms_recipe(self, client_socket, request):
        role_name = request.get("role_name")
        recipe = self.db_handler.get_moms_recipe()
        print(recipe)
        response = {"status": "success", "feedback": recipe}
        client_socket.sendall(json.dumps(response).encode())