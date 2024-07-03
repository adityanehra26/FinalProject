from userHandler.user import User
from menuItems.food_menu import FoodMenu

class Employee(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)
        self.food_menu = FoodMenu(server_communicator, self.role)

    def user_menu(self):
        print(f"\nWelcome {self.name}({self.role})!")
        while True:
            print("\n1. Food Selection\n2. See Feedback\n3. Food Selection for tomorrow\n4. Exit/Logout")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                print("Food Selection")
            elif(choice == 2):
                self.food_menu.view_feedback()
            elif(choice == 3):
                self.food_menu.vote_for_menu()
            elif(choice == 4):
                print("\nEXITING...")
                self.server_communicator.close_connection()
                break


