import json
class MenuManager:
    def __init__(self, server_communicator, role, user_id):
        self.server_communicator = server_communicator
        self.role = role
        self.user_id = user_id

    def add_menu_item(self):
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
        data = {"Name": food_name, "Price": price, "MealTypeID": mealtypeid, "RoleName": "Admin", "AvailabilityStatus": 1}
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    def delete_menu_item(self):
        item_id = int(input("Please enter food ID : "))
        endpoint = "/delete-menu-item"
        data = {"RoleName": "Admin", "MenuItemID": item_id}
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    def update_menu_item(self):
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
        
    def update_item_availability(self):
        item_id = int(input("Please enter food ID to Update : "))
        endpoint = "/update-availability"
        availability = input("Enter availability (Yes or No)")
        if availability.upper() == "YES":
            availability = 1
        elif availability.upper() == "NO":
            availability = 0
        else: 
            print("Invalid Input")
            return 
        data = {"RoleName": "Chef", "MenuItemID": item_id, "AvailabilityStatus": availability}

        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    def add_moms_recipe(self):
        print("Enter the mom's recipe (press Enter once to finish):")
        recipe = []

        while True:
            line = input()
            if line == "": 
                break
            recipe.append(line)
        
        recipe_text = "\n".join(recipe) 

        print("\nRecipe entered:")
        print(recipe_text)

        data = {
            "UserID": self.user_id,
            "Recipe": recipe_text,
            "RoleName": self.role
        }

        endpoint = "/add-moms-recipe"
        response = self.server_communicator.send_request(endpoint, data)

        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])

    

