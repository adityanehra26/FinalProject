from userHandler.user import User
from menuItems.food_menu import FoodMenu
from utility.notification_handler import NotificationHandler
class Employee(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)
        self.food_menu = FoodMenu(server_communicator, self.role, self.id)
        self.notification_handler = NotificationHandler(server_communicator)

    def user_menu(self):
        print(f"\nWelcome {self.name}({self.role})!")
        while True:
            notifications = self.notification_handler.get_notification()
            if notifications:
                print("\nNOTIFICATIONS\n=============")
                for notification in notifications:
                    print(notification[1])
            else:
                print()
            print("\n1. View Menu Item\n2. Update Profile \n3. Food Recommendation for Tomorrow\n4. Give Feedback\n5. View Feedback\n6. Exit")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                self.food_menu.view_menu()
            elif choice == 2:
                self.food_menu.update_user_profile()    
            elif choice == 3:
                self.food_menu.vote_for_menu()
            elif choice == 4:
                self.food_menu.give_feedback()
            elif choice == 5:
                self.food_menu.view_feedback()
            elif(choice == 6):
                print("\nEXITING...Bye")
                self.server_communicator.close_connection()
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")


