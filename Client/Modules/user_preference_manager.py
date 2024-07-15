import json 

class UserPreferenceManager:
    def __init__(self, server_communicator, role, user_id):
        self.server_communicator = server_communicator
        self.role = role
        self.user_id = user_id

    def update_user_profile(self):
            endpoint = "/update-user-profile"
            print("updateeeee")
            diet_preference= self.get_diet_preference()
            spice_level= self.get_spice_level()
            
            cuisine_preference= self.get_cuisine_preference()
            sweet_tooth= self.get_sweetness_preference()
            data = {
                "RoleName": "Employee",
                "UserId": self.user_id,
                "DietPreference": diet_preference,
                "SpiceLevel": spice_level,
                "CuisinePreference": cuisine_preference,
                "SweetTooth": sweet_tooth
            }
            response = self.server_communicator.send_request(endpoint, data)
            if response["status"] == "success":
                print(response["message"])
            else:
                print(response["message"])

    def get_diet_preference(self):           
        while 1:
            print("\nPlease select your diet preference:\n1. Vegetarian\n2. Non-Vegetarian\n3. Eggetarian")
            spice_level_choice = int(input("Enter choice (1/2/3): "))
            if spice_level_choice == 1:
                return "Vegetarian"
            elif spice_level_choice == 2:
                return "Non-Vegetarian"
            elif spice_level_choice == 3:
                return "Eggetarian"
            else:
                print("Invalid Input")

    def get_spice_level(self):
        while 1:
            print("\nPlease select your spice level:\n1. High\n2. Medium\n3. Low")
            spice_level_choice = int(input("Enter choice (1/2/3): "))
            if spice_level_choice == 1:
                return "High"
            elif spice_level_choice == 2:
                return "Medium"
            elif spice_level_choice == 3:
                return "Low"
            else:
                print("Invalid Input")
                
    def get_cuisine_preference(self):
        while 1:
            print("\nWhat do you prefer most?\n1. North Indian\n2. South Indian\n3. Other")
            cuisine_preference_choice = int(input("Enter choice (1/2/3): "))
            if cuisine_preference_choice == 1:
                return "North Indian"
            elif cuisine_preference_choice == 2:
                return "South Indian"
            elif cuisine_preference_choice == 3:
                return "Other"
            else:
                print("Invalid Input")
            
    def get_sweetness_preference(self):
        while 1:
            print("\nDo you have a sweet tooth?\n1. Yes\n2. No")
            sweet_tooth_choice = int(input("Enter choice (1/2): "))
            if sweet_tooth_choice == 1:
                return 1
            elif sweet_tooth_choice == 2:
                return 0
            else:
                print("Invalid Input")
                