import json
class MenuManager:
    def __init__(self, server_communicator, role, user_id):
        self.server_communicator = server_communicator
        self.role = role
        self.user_id = user_id

    def delete_menu_item(self):
        item_id = int(input("Please enter food ID : "))
        endpoint = "/delete-menu-item"
        data = {"RoleName": "Admin", "MenuItemID": item_id}
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])
            
    def add_menu_item(self):
        food_name = ""
        while not food_name:
            food_name_input = input("Enter the food item name: ").strip().title()
            food_name = food_name_input

        price = input("Enter Price: ")
        mealtypeid = self.get_mealtype_id()
        diet_preference = self.get_diet_preference()
        spice_level = self.get_spice_level()
        cuisine_preference = self.get_cuisine_preference()
        sweet_tooth_status = self.get_sweet_tooth_status()

        endpoint = "/add-menu-item"
        data = {
            "Name": food_name,
            "Price": price,
            "MealTypeID": mealtypeid,
            "RoleName": "Admin",
            "AvailabilityStatus": 1,
            "DietPreference": diet_preference,
            "SpiceLevel": spice_level,
            "CuisinePreference": cuisine_preference,
            "SweetTooth": sweet_tooth_status
        }
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])
        
    
    def update_menu_item(self):
        item_id = int(input("Please enter food ID to Update: "))
        endpoint = "/update-menu-item"

        price = int(input("Enter new price: "))  
        availability_status = self.get_availability_status()
        diet_preference = self.get_diet_preference()
        spice_level = self.get_spice_level()
        cuisine_preference = self.get_cuisine_preference()
        sweet_tooth_status = self.get_sweet_tooth_status()
    
        data = {
            "RoleName": "Admin", 
            "MenuItemID": item_id,
            "Price": price, 
            "AvailabilityStatus": availability_status,
            "DietPreference": diet_preference,
            "SpiceLevel": spice_level,
            "CuisinePreference": cuisine_preference,
            "SweetTooth": sweet_tooth_status
        }
    
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])
    
    def get_mealtype_id(self):
        mealtype = ""
        while mealtype not in ["BREAKFAST", "LUNCH", "DINNER"]:
            mealtype = input("Meal Type (Breakfast, Lunch, Dinner): ").strip().upper()
            if mealtype not in ["BREAKFAST", "LUNCH", "DINNER"]:
                print("Invalid Meal Type. Please enter again.")
        
        mealtypeid = 0
        if mealtype == "BREAKFAST":
            mealtypeid = 1
        elif mealtype == "LUNCH":
            mealtypeid = 2
        elif mealtype == "DINNER":
            mealtypeid = 3
        return mealtypeid
    
    def get_availability_status(self):
        availability = ""
        while availability not in ["YES", "NO"]:
            availability = input("Enter availability (Yes or No): ").strip().upper()
            if availability not in ["YES", "NO"]:
                print("Invalid input. Please enter Yes or No.")
        return 1 if availability == "YES" else 0
    
    def get_diet_preference(self):
        diet_preference = ""
        while diet_preference not in ["VEGETARIAN", "NON-VEGETARIAN", "EGGETARIAN"]:
            diet_preference = input("Enter diet preference (Vegetarian, Non-Vegetarian, Eggetarian): ").strip().upper()
            if diet_preference not in ["VEGETARIAN", "NON-VEGETARIAN", "EGGETARIAN"]:
                print("Invalid input. Please enter Vegetarian, Non-Vegetarian, or Eggetarian.")
        return diet_preference.capitalize()
    
    def get_spice_level(self):
        spice_level = ""
        while spice_level not in ["LOW", "MEDIUM", "HIGH"]:
            spice_level = input("Enter spice level (Low, Medium, High): ").strip().upper()
            if spice_level not in ["LOW", "MEDIUM", "HIGH"]:
                print("Invalid input. Please enter Low, Medium, or High.")
        return spice_level.capitalize()
    
    def get_cuisine_preference(self):
        cuisine_preference = ""
        while cuisine_preference not in ["NORTH INDIAN", "SOUTH INDIAN", "WEST INDIAN"]:
            cuisine_preference = input("Enter cuisine preference (North Indian, South Indian, West Indian): ").strip().upper()
            if cuisine_preference not in ["NORTH INDIAN", "SOUTH INDIAN", "WEST INDIAN"]:
                print("Invalid input. Please enter North Indian, South Indian, or West Indian.")
        return cuisine_preference.capitalize()
    
    def get_sweet_tooth_status(self):
        sweet_tooth = ""
        while sweet_tooth not in ["YES", "NO"]:
            sweet_tooth = input("Enter sweet tooth preference (Yes or No): ").strip().upper()
            if sweet_tooth not in ["YES", "NO"]:
                print("Invalid input. Please enter Yes or No.")
        return 1 if sweet_tooth == "YES" else 0
        
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

    

