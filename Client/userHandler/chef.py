from userHandler.user import User
from Modules.menu_viewer import MenuViewer
from Modules.feedback_handler import FeedbackHandler
from Modules.menu_manager import MenuManager
from Modules.roll_out_manager import RolloutManager
from Modules.user_preference_manager import UserPreferenceManager
from Modules.voting_handler import VotingHandler
from utility.notification_handler import NotificationHandler

class Chef(User):
    def __init__(self, id, name, role, server_communicator):
        super().__init__(id, name, role, server_communicator)
        self.user_manager = UserPreferenceManager(server_communicator, self.role, self.id)
        self.menu_manager = MenuManager(server_communicator, self.role, self.id)
        self.notification_handler = NotificationHandler(server_communicator)
        self.menu_viewer = MenuViewer(server_communicator, self.role)
        self.feedback_handler = FeedbackHandler(server_communicator, self.role, self.id)
        self.roll_out_manager = RolloutManager(server_communicator, self.role, self.id)
        self.voting_handler = VotingHandler(server_communicator, self.role, self.id)


    def user_menu(self):
        print(f"\nWelcome {self.name}({self.role})!")
        while True:
            print("\n1. View Menu Item\n2. Roll Out Tomorrow's Menu\n3. View Yesterday's Vote \n4. Update Availability of Menu Item\n5. View Feedback\n6. View Discard Item\n7. Delete Menu Item\n8. View Mom's Recipes\n9. Exit")
            choice = int(input("Enter a choice : "))
            if(choice == 1):
                self.menu_viewer.view_menu()
            elif(choice == 2):
                self.roll_out_manager.roll_out_menu()
            elif choice == 3:
                self.voting_handler.view_yesterday_voting()
            elif choice == 4:
                self.menu_manager.update_item_availability()
            elif choice == 5:
                self.feedback_handler.view_feedback()
            elif choice == 6:
                self.menu_viewer.view_low_rating_items()
            elif choice == 7:
                self.menu_manager.delete_menu_item()
            elif choice == 8:
                self.menu_viewer.view_momsrecipe()
            elif choice == 9:
                print("\nEXITING...Bye")
                self.server_communicator.close_connection()
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")


