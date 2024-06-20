from userHandler.user import User

class Employee(User):
    def __init__(self, id, name, role, client_socket):
        super().__init__(id, name, role, client_socket)

    def user_menu(self):
        print(f"\nWelcome {self.name}!")
        while True:
            print("\n1. Food Selection\n2. See Feedback\n4. Exit/Logout")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                print("Food Selection")
            elif(choice == 2):
                print("See Feeback")
            elif(choice == 4):
                print("\nEXITING...")
                self.client_socket.close_connection()
                exit


