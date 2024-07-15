import json
class FeedbackHandler:
    def __init__(self, server_communicator, role, user_id):
        self.server_communicator = server_communicator
        self.user_id = user_id
        self.role = role

    def give_feedback(self):
        menu_item_id = input("Enter the Menu Item ID: ")
        rating = input("Enter your Rating (e.g., 4.5): ")
        comment = input("Enter your Comment: ")

        endpoint = "/give-feedback"
        data = {
            "UserID": self.user_id,
            "MenuItemID": int(menu_item_id),
            "Rating": float(rating),
            "Comment": comment,
            "RoleName": "Employee"
        }

        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    def view_feedback(self):
        endpoint = "/view-feedback"
        data = {"role_name": self.role}
        response = self.server_communicator.send_request(endpoint, data)
        
        if response["status"] == "success":
            print(f"{'FoodName':<35} {'UserName':<35} {'Rating':<10} {'Comment':<70} {'Date':<20}")
            for item in response['feedback']:
                print(f"{item['FoodName']:<35} {item['UserName']:<35} {item['Rating']:<10} {item['Comment']:<70} {item['Date']:<20}")
        else:
            print("Failed to fetch feedback: ", response["message"])