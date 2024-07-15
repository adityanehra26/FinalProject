import json 

class FoodMenu:
    def __init__(self, server_communicator, role, user_id):
        self.server_communicator = server_communicator
        self.role = role
        self.user_id = user_id

    def view_low_rating_items(self):
        endpoint = "/view-low-rating-items"
        data = {"role_name": self.role}
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(f"{'FoodName':<35} {'AvgRating':<10}")
            for item in response['low_rating_items']:
                print(f"{item['FoodName']:<35} {item['AvgRating']:<10.2f}")
        else:
            print("Failed to fetch low rating items: ", response["message"])

    def view_menu(self):
        endpoint = "/food_menu"
        data = {"role_name": self.role}
        response = self.server_communicator.send_request(endpoint, data)
        
        print(f"{'ID':<5} {'Name':<35} {'Price':<10} {'AvailabilityStatus':<20}")
        
        for item in response['menu']:
            availability = "Yes" if item['AvailabilityStatus'] == 1 else "No"
            print(f"{item['ID']:<5} {item['Name']:<35} {item['Price']:<10} {availability:<20}")

    def view_feedback(self):
        endpoint = "/view-feedback"
        data = {"role_name": self.role}
        print(endpoint, data)
        response = self.server_communicator.send_request(endpoint, data)
        print(f"{'FoodName':<35} {'UserName':<25} {'Rating':<10} {'Comment':<70} {'Date':<20}")
        
        for item in response['feedback']:
            print(f"{item['FoodName']:<35} {item['UserName']:<25} {item['Rating']:<10} {item['Comment']:<70} {item['Date']:<20}")

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

    def update_availabilty(self):
        self.view_menu()
        item_id = int(input("Please enter food ID to Update : "))
        endpoint = "/update-availablity"
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


    def update_user_profile(self):
        endpoint = "/update-user-profile"
        # Diet Preference
        print("Please select one:")
        print("1. Vegetarian")
        print("2. Non Vegetarian")
        print("3. Eggetarian")
        diet_preference_choice = int(input("Enter choice (1/2/3): "))
        if diet_preference_choice == 1:
            new_dietpreference = "Vegetarian"
        elif diet_preference_choice == 2:
            new_dietpreference = "Non Vegetarian"
        elif diet_preference_choice == 3:
            new_dietpreference = "Eggetarian"
        else:
            print("Invalid Input")
            return
        
        # Spice Level
        print("Please select your spice level:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        spice_level_choice = int(input("Enter choice (1/2/3): "))
        if spice_level_choice == 1:
            new_spicelevel = "High"
        elif spice_level_choice == 2:
            new_spicelevel = "Medium"
        elif spice_level_choice == 3:
            new_spicelevel = "Low"
        else:
            print("Invalid Input")
            return
        
        # Cuisine Preference
        print("What do you prefer most?")
        print("1. North Indian")
        print("2. South Indian")
        print("3. Other")
        cuisine_preference_choice = int(input("Enter choice (1/2/3): "))
        if cuisine_preference_choice == 1:
            new_cuisinepreference = "North Indian"
        elif cuisine_preference_choice == 2:
            new_cuisinepreference = "South Indian"
        elif cuisine_preference_choice == 3:
            new_cuisinepreference = "Other"
        else:
            print("Invalid Input")
            return
        
        # Sweet Tooth
        print("Do you have a sweet tooth?")
        print("1. Yes")
        print("2. No")
        sweet_tooth_choice = int(input("Enter choice (1/2): "))
        if sweet_tooth_choice == 1:
            new_sweettooth = 1
        elif sweet_tooth_choice == 2:
            new_sweettooth = 0
        else:
            print("Invalid Input")
            return

        data = {
            "RoleName": "Employee",
            "UserId": self.user_id,
            "DietPreference": new_dietpreference,
            "SpiceLevel": new_spicelevel,
            "CuisinePreference": new_cuisinepreference,
            "SweetTooth": new_sweettooth
        }
        print(data)
        response = self.server_communicator.send_request(endpoint, data)
        if response["status"] == "success":
            print(response["message"])
        else:
            print(response["message"])
