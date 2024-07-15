class MenuViewer:
    def __init__(self, server_communicator, role):
        self.server_communicator = server_communicator
        self.role = role

    def view_menu(self):
        endpoint = "/food_menu"
        data = {"role_name": self.role}
        response = self.server_communicator.send_request(endpoint, data)
        print(f"{'ID':<5} {'Name':<35} {'Price':<10} {'AvailabilityStatus':<20}")
        for item in response['menu']:
            availability = "Yes" if item['AvailabilityStatus'] == 1 else "No"
            print(f"{item['ID']:<5} {item['Name']:<35} {item['Price']:<10} {availability:<20}")

    def view_low_rating_items(self):
        endpoint = "/view-low-rating-items"
        data = {"role_name": self.role}
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(f"{'FoodName':<35} {'OverallRating':<10}")
            for item in response['low_rating_items']:
                print(f"{item['FoodName']:<35} {item['AvgRating']:<10.2f}")
        else:
            print("Failed to fetch low rating items: ", response["message"])

    def view_momsrecipe(self):
        endpoint = "/view-moms-recipe"
        response = self.server_communicator.send_request(endpoint)
        print(f"{'ID':<10} {'UserName':<25} {'Recipe':<70}")
        for item in response['feedback']:
            print(f"{item['UserID']:<10} {item['UserName']:<25} {item['Recipe']:<70}")
