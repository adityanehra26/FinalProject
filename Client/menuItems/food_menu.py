import json 

class FoodMenu:
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

    
    def add_food_item(self):
        food_name = input("Enter the food item name : ")
        price = input("Enter Price : ")
        mealtype = input("Meal Type : ")
        mealtypeid = 0
        if mealtype.upper() == "BREAKFAST":
            mealtypeid = 1
        elif mealtype.upper() == "LUNCH":
            mealtypeid = 2
        elif mealtype.upper() == "DINNER":
            mealtypeid = 3

        endpoint = "/add-menu-item"
        data = { "Name": food_name, "Price": price, "MealTypeID": mealtypeid, "RoleName": "Admin", "AvailabilityStatus": 1}

        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    def delete_menu_item(self):
        self.view_menu()
        item_id = int(input("Please enter food ID : "))
        endpoint = "/delete-menu-item"
        data = {"RoleName": "Admin", "MenuItemID": item_id}

        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])
    
    def update_menu_item(self):
        self.view_menu()
        item_id = int(input("Please enter food ID to Update : "))
        endpoint = "/update-menu-item"
        new_price = int(input("Enter new price : "))
        availability = input("Enter availability (Yes or No)")
        if availability.upper() == "YES":
            availability = 1
        elif availability.upper() == "NO":
            availability = 0
        else: 
            print("Invalid Input")
            return 
        data = {"RoleName": "Admin", "MenuItemID": item_id, "Price": new_price, "AvailabilityStatus": availability}

        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

