from userHandler.user import User

class Admin(User):
    def __init__(self, id, name, role, client_socket):
        super().__init__(id, name, role, client_socket)

    def user_menu(self):
        print(f"\nWelcome {self.name}!")
        while True:
            print("\n1. View Menu\n2. Add Menu Item\n3. Delete Menu Item\n4. Delete Menu Item\n5. Exit/Logout")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                print("View Menu")
            elif(choice == 2):
                print("Add Menu Item")
            elif(choice == 3):
                print("Delete Menu Item")
            elif(choice == 4):
                print("Updatingg")
            elif(choice == 5):
                print("\nEXITING...")
                self.client_socket.close_connection()
                exit


