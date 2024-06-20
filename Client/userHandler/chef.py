from userHandler.user import User

class Chef(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)

    def user_menu(self):
        print(f"\nWelcome {self.name}({self.role})!")
        print("\n1. View Menu\n2. Feedbacks\n3. RollOut Menu\n4. Exit/Logout")
        choice = int(input("Enter a choice : "))
        if(choice == 1):
            print("Viewing Menu")
        elif(choice == 2):
            print("See Feeback")
        elif(choice == 3):
            print("Rolling out menu")
        elif(choice == 4):
            print("\nEXITING...")
            self.server_communicator.close_connection()
            exit


