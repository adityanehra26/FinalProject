from userHandler.user import User
from menuItems.food_menu import FoodMenu

class Chef(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)
        self.food_menu = FoodMenu(server_communicator, self.role, self.id)

    def user_menu(self):
        print(f"\nWelcome {self.name}({self.role})!")
        while True:
            print("\n1. View Menu Item\n2. Roll Out Tomorrow's Menu\n3. View Yesterday's Vote \n4. Update Availability of Menu Item\n5. View Feedback\n6. View Discard Item\n7. Exit")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                self.food_menu.view_menu()
            elif(choice == 2):
                self.food_menu.roll_out_menu()
            elif choice == 3:
                self.food_menu.view_yesterday_voting()
            elif choice == 4:
                self.food_menu.update_availabilty()
            elif choice == 5:
                self.food_menu.view_feedback()
            elif choice == 6:
                self.food_menu.view_low_rating_items()
            elif choice == 7:
                print("\nEXITING...Bye")
                self.server_communicator.close_connection()
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")


