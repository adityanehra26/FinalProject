import json
class VotingHandler:
    def __init__(self, db_handler):
        self.db_handler= db_handler

    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/voting":
            self.vote_for_menu(client_socket, request)
        elif endpoint == "/voting-items":
            self.view_voting_items(client_socket, request)

    def vote_for_menu(self, client_socket, request):
        data = request.get("data")
        print(data)
        if not data:
            raise ValueError("No data provided")
        try:
            for meal_type, menu_item_id in data.items():
                menu_item_id = int(menu_item_id)
                result = self.db_handler.add_vote(menu_item_id)
                if result != "success":
                    response = {"status": "failure", "message": f"Failed to cast vote for {meal_type}"}
                    client_socket.sendall(json.dumps(response).encode())
                    return

            response = {"status": "success", "message": "Votes successfully cast"}
        except Exception as e:
            print(f"Error in vote_for_menu: {e}")
            response = {"status": "failure", "message": "An error occurred while casting votes"}
        client_socket.sendall(json.dumps(response).encode())

    def view_voting_items(self, client_socket, request):
        user_id = request.get("UserID")
        try:
            diet_preference = self.db_handler.get_diet_preference(user_id)
            voting_items = self.db_handler.get_voting_items(diet_preference)
            categorized_items = {"Breakfast": [], "Lunch": [], "Dinner": []}

            for item in voting_items:
                meal_type = item[2]
                categorized_items[meal_type].append({
                    "MenuItemID": item[0],
                    "MenuItemName": item[1],
                    "Votes": item[3]
                })

            response = {"status": "success", "data": categorized_items}
            client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error in view_voting_items: {e}")
            response = {"status": "failure", "message": "An error occurred while fetching voting items"}
            client_socket.sendall(json.dumps(response).encode())

      