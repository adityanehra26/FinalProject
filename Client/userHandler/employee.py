from userHandler.user import User
from menuItems.food_menu import FoodMenu
from utility.notification_handler import NotificationHandler

class Employee(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)
        self.food_menu = FoodMenu(server_communicator, self.role)
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
            print("\n1. Food Selection\n2. See Feedback\n3. Food Selection for tomorrow\n4. Exit/Logout")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                print("Food Selection")
            elif(choice == 2):
                self.food_menu.view_feedback()
            elif(choice == 3):
                self.food_menu.vote_for_menu(self.id)
            elif(choice == 4):
                print("\nEXITING...")
                self.server_communicator.close_connection()
                break
            else:
                print("\nInvalid Choice")


