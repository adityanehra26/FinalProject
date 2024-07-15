import json 

class VotingHandler:
    def __init__(self, server_communicator, role, user_id):
        self.server_communicator = server_communicator
        self.role = role
        self.user_id = user_id

    def view_voting_items(self):
        endpoint = "/voting-items"
        data = {"UserID": self.user_id}
        response = self.server_communicator.send_request(endpoint, data)
        response = response["data"]
        voting_items = {"Breakfast": [], "Lunch": [], "Dinner": []}

        print("Breakfast Recommendations")
        print(f"{'MenuItemID':<10} {'Name':<35}")
        for item in response['Breakfast']:
            print(f"{item['MenuItemID']:<10} {item['MenuItemName']:<35}")
            voting_items['Breakfast'].append(item)

        print("Lunch Recommendations")
        print(f"{'MenuItemID':<10} {'Name':<35} ")
        for item in response['Lunch']:
            print(f"{item['MenuItemID']:<10} {item['MenuItemName']:<35} ")
            voting_items['Lunch'].append(item)

        print("Dinner Recommendations")
        print(f"{'MenuItemID':<10} {'Name':<35}")
        for item in response['Dinner']:
            print(f"{item['MenuItemID']:<10} {item['MenuItemName']:<35} ")
            voting_items['Dinner'].append(item)

        return voting_items

    def vote_for_menu(self):
        voting_items = self.view_voting_items()
        votes = {}
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            valid_choices = [str(item['MenuItemID']) for item in voting_items[meal_type]]
            while True:
                menu_item_id = input(f"Enter the ID for {meal_type} ({', '.join(valid_choices)}): ")
                if menu_item_id in valid_choices:
                    votes[meal_type] = menu_item_id
                    break
                else:
                    print(f"Incorrect choice. Please enter a valid ID for {meal_type} ({', '.join(valid_choices)}).")

        endpoint = "/voting"
        data = {"employee_id": self.user_id, "data": votes}
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    def view_yesterday_voting(self):
        endpoint = "/voting-items"
        data = {}
        response = self.server_communicator.send_request(endpoint, data)
        categorized_items = response['data']

        for meal_type, items in categorized_items.items():
            print(f"\n{meal_type} Recommendations")
            print(f"{'MenuItemID':<10} {'Name':<35} {'Votes':<5}")
            for item in items:
                print(f"{item['MenuItemID']:<10} {item['MenuItemName']:<35} {item['Votes']:<5}")
