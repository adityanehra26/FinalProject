class RolloutManager:
    def __init__(self, server_communicator, role, user_id):
        self.server_communicator = server_communicator
        self.role = role
        self.user_id = user_id

    def get_recomendation(self):
        endpoint = "/view-recomendation"
        data = {"RoleName": self.role}
        response = self.server_communicator.send_request(endpoint, data)
        print("\nBreakfast Recommendations\n")
        print(f"{'ID':<5} {'Name':<35}")

        food_id_for_roll_out = {"Breakfast": [], "Lunch": [], "Dinner": []}
        for item in response['recomendations']['Breakfast']:
            print(f"{item['ID']:<5} {item['Name']:<35}")

        food_id_for_roll_out["Breakfast"] = input("Enter the Two ID for breakfast: ").split()

        print("\nLunch Recommendations")
        for item in response['recomendations']['Lunch']:
            print(f"{item['ID']:<5} {item['Name']:<35}")

        food_id_for_roll_out["Lunch"] = input("Enter the ID for Lunch: ").split()

        print("\nDinner Recommendations")
        for item in response['recomendations']['Dinner']:
            print(f"{item['ID']:<5} {item['Name']:<35}")

        food_id_for_roll_out["Dinner"] = input("Enter the ID for Dinner: ").split()

        return food_id_for_roll_out

    def roll_out_menu(self):
        food_id_for_roll_out = self.get_recomendation()
        endpoint = "/roll-out"
        data = {"data": food_id_for_roll_out}
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])