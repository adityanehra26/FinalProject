from userHandler.user import User
from Modules.menu_manager import MenuManager
from Modules.menu_viewer import MenuViewer

class Admin(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)
        self.menu_viewer = MenuViewer(server_communicator, self.role)
        self.menu_manager = MenuManager(server_communicator, self.role, self.id)

    def user_menu(self):
        print(f"\nWelcome {self.name}({self.role})!")
        while True:
            print("\n1. View Menu\n2. Add Menu Item\n3. Delete Menu Item\n4. Update Menu Item\n5. View Discard Item\n6. View Mom's Recipes\n7. Exit")
            choice = int(input("Enter a choice : "))
            if choice == 1:
                self.menu_viewer.view_menu()
            elif choice == 2:
                self.menu_manager.add_menu_item()
            elif choice == 3:
                self.menu_manager.delete_menu_item()
            elif choice == 4:
                self.menu_manager.update_menu_item()
            elif choice == 5:
                self.menu_viewer.view_low_rating_items()
            elif choice == 6:
                self.menu_viewer.view_momsrecipe()
            elif choice == 7:
                print("\nEXITING...Bye")
                self.server_communicator.close_connection()
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")




