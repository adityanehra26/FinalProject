from userHandler.user import User
from menuItems.food_menu import FoodMenu

class Admin(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)
        self.food_menu = FoodMenu(server_communicator, self.role, self.id)

    def user_menu(self):
        print(f"\nWelcome {self.name}({self.role})!")
        while True:
            print("\n1. View Menu\n2. Add Menu Item\n3. Delete Menu Item\n4. Update Menu Item\n5. View Discard Item\n6. Exit")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                self.food_menu.view_menu()
            elif(choice == 2):
                self.food_menu.add_food_item()
            elif(choice == 3):
                self.food_menu.delete_menu_item()
            elif(choice == 4):
                self.food_menu.update_menu_item()
            elif(choice == 5):
                self.food_menu.view_low_rating_items()
            elif(choice == 6):
                print("\nEXITING...Bye")
                self.server_communicator.close_connection()
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")



