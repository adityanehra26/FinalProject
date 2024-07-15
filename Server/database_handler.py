import mysql.connector
from datetime import datetime

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connection established")
        except mysql.connector.Error as err:
            print(f"Error: Could not establish connection: {err}")

    def check_login(self, username, password):
        cursor = self.conn.cursor()
        query = """
        SELECT u.ID, u.Name, r.RoleName
        FROM user u
        JOIN Role r ON u.RoleID = r.ID
        WHERE u.Name=%s AND u.Password=%s
        """
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {"ID": result[0], "Name": result[1], "RoleName": result[2]}
        return None
    
    def get_food_menu(self):
        cursor = self.conn.cursor()
        query = "SELECT ID, Name, Price, AvailabilityStatus FROM menuitem"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        menu = []
        for item in result:
            menu.append({
                "ID": item[0],
                "Name": item[1],
                "Price": item[2],
                "AvailabilityStatus": item[3]
            })
        return menu
    
    def get_feedback_details(self):
        cursor = self.conn.cursor()
        query = """
        SELECT 
            f.ID,
            u.Name AS UserName,
            m.Name AS FoodName,
            f.Rating,
            f.Comment,
            f.Date
        FROM 
            feedback f
        JOIN 
            user u ON f.UserID = u.ID
        JOIN 
            menuitem m ON f.MenuItemID = m.ID
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        feedback_details = []
        for item in result:
            feedback_details.append({
                "FeedbackID": item[0],
                "UserName": item[1],
                "FoodName": item[2],
                "Rating": item[3],
                "Comment": item[4],
                "Date": item[5].strftime('%Y-%m-%d')  # Convert date to string
            })
        return feedback_details
    

    def give_menuItemfeedback(self, data):
        cursor = self.conn.cursor()
        query = """
        INSERT INTO feedback (UserID, MenuItemID, Rating, Comment, Date)
        VALUES (%s, %s, %s, %s, %s)
        """
        current_date = datetime.now().date()  # Get current date
        values = (data["UserID"], data["MenuItemID"], float(data["Rating"]), data["Comment"], current_date)
        
        try:
            cursor.execute(query, values)
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"An error occurred while inserting feedback: {e}")
            self.conn.rollback()
            return "error"
        finally:
            cursor.close()

    
    def add_menuItem(self, data):
        cursor = self.conn.cursor()
        query = """
        INSERT INTO menuitem (Name, Price, AvailabilityStatus, MealTypeID)
        VALUES (%s, %s, %s, %s)
        """
        values = (data["Name"], int(data["Price"]), data["AvailabilityStatus"], data["MealTypeID"])
        try:
            cursor.execute(query, values)
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
            return "error"
    
    def delete_menuItem(self, menu_item_id):
        cursor = self.conn.cursor()
        delete_feedback_query = """
        DELETE FROM feedback
        WHERE MenuItemID = %s
        """
        delete_menu_item_query = """
        DELETE FROM menuitem
        WHERE ID = %s
        """
        try:
            cursor.execute(delete_feedback_query, (menu_item_id,))
            cursor.execute(delete_menu_item_query, (menu_item_id,))
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
            return "error"
        finally:
            cursor.close()

    def update_menuItem(self, menu_item_id, new_price, new_availability):
        cursor = self.conn.cursor()
        update_query = """
        UPDATE menuitem
        SET Price = %s, AvailabilityStatus = %s
        WHERE ID = %s
        """
        try:
            cursor.execute(update_query, (new_price, new_availability, menu_item_id))
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
            return "error"
        finally:
            cursor.close()
            
    def update_menuItemavailabilty(self, menu_item_id, new_availability):
        cursor = self.conn.cursor()
        update_query = """
        UPDATE menuitem
        SET AvailabilityStatus = %s
        WHERE ID = %s
        """
        try:
            cursor.execute(update_query, (new_availability, menu_item_id))
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
            return "error"
        finally:
            cursor.close()
        
            
    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connection closed")
    
    def calculate_average_ratings(self):
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT m.ID AS MenuItemID, m.Name AS MenuItem, AVG(f.Rating) AS AvgRating, f.Comment, m.MealTypeID
            FROM feedback f
            JOIN menuitem m ON f.MenuItemID = m.ID
            GROUP BY f.MenuItemID, m.Name, f.Comment, m.MealTypeID;
        """
        cursor.execute(query)
        avg_ratings = cursor.fetchall()
        cursor.close()
        print(avg_ratings)
        return avg_ratings

    def add_recommended_menu_item(self, menu_item_id, votes):
        cursor = self.conn.cursor()
        query = "INSERT INTO recommendedmenuitem (MenuItemID, Votes) VALUES (%s, %s)"
        try:
            cursor.execute(query, (menu_item_id, votes))
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"Error in add_recommended_menu_item: {e}")
            self.conn.rollback()
            return "error"
        finally:
            cursor.close()

    def truncate_recommended_menu_item_table(self):
        try:
            if self.conn is None or not self.conn.is_connected():
                raise Exception("MySQL Connection not available")

            cursor = self.conn.cursor()
            cursor.execute("TRUNCATE TABLE recommendedmenuitem")
            self.conn.commit()
            return "success"
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "failure"
        except Exception as e:
            print(f"Error: {e}")
            return "failure"

        
    def get_voting_items(self, diet_preference):
        query = """
        SELECT ri.MenuItemID, mi.Name as MenuItemName, m.MealType, ri.Votes, 
            (mi.DietPreference = %s) AS is_preferred
        FROM recommendedmenuitem ri
        JOIN menuitem mi ON ri.MenuItemID = mi.ID
        JOIN mealtype m ON mi.MealTypeID = m.ID
        ORDER BY is_preferred DESC, m.MealType, mi.Name
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (diet_preference,))
        return cursor.fetchall()

    def add_vote(self, menu_item_id):
        query = "UPDATE recommendedmenuitem SET Votes = Votes + 1 WHERE MenuItemID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (menu_item_id,))
        self.conn.commit()
        return "success"

    def reset_form_filled_status_for_all_user(self):
        query = "UPDATE user SET FormFilledStatus = 0"
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        return "success"

    def check_form_filled_status(self, user_id):
        query = "SELECT FormFilledStatus FROM user WHERE ID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0]
    
    def update_form_filled_status(self, user_id, status):
        query = "UPDATE user SET FormFilledStatus = %s WHERE ID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (status, user_id))
        self.conn.commit()
        return "success"
    
    def send_notification(self, message):
        cursor = self.conn.cursor()
        print("send_notification")
        today_date = datetime.today().strftime('%Y-%m-%d')
        query = "INSERT INTO notification (Message, Date) VALUES (%s, %s)"
        cursor.execute(query, (message, today_date))
        self.conn.commit()
        cursor.close()

    def get_notification(self):
        cursor = self.conn.cursor()
        today_date = datetime.today().strftime('%Y-%m-%d')
        query = "SELECT ID, Message, Date FROM notification WHERE Date = %s"
        cursor.execute(query, (today_date,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def update_userprofile(self, user_id, new_dietpreference, new_spicelevel, new_cuisinepreference, new_sweettooth):
        cursor = self.conn.cursor()
        print((new_dietpreference, new_spicelevel, new_cuisinepreference, new_sweettooth, user_id))
        update_query = """
        UPDATE user
        SET DietPreference = %s, SpiceLevel = %s, CuisinePreference = %s, SweetTooth = %s
        WHERE ID = %s
        """
        try:
            cursor.execute(update_query, (new_dietpreference, new_spicelevel, new_cuisinepreference, new_sweettooth, user_id))
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
            return "error"
        finally:
            cursor.close()

    def get_diet_preference(self, user_id):
        query = "SELECT DietPreference FROM user WHERE ID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None       
    
    def get_low_rating_items(self):
        cursor = self.conn.cursor()
        query = """
        SELECT m.ID AS MenuItemID, m.Name AS MenuItem, AVG(f.Rating) AS AvgRating, f.Comment, m.MealTypeID
        FROM feedback f
        JOIN menuitem m ON f.MenuItemID = m.ID
        GROUP BY f.MenuItemID, m.Name, f.Comment, m.MealTypeID
        HAVING Avg(f.Rating) <= 2;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        low_rating_items = []
        for item in result:
            low_rating_items.append({
                "MenuItemID": item[0],
                "FoodName": item[1],
                "AvgRating": item[2]
            })
        return low_rating_items

    def add_moms_recipe(self, user_id, moms_recipe):
        cursor = self.conn.cursor()
        query = """
        INSERT INTO momsrecipe (UserID, MomsRecipe)
        VALUES (%s, %s)
        """
        try:
            cursor.execute(query, (user_id, moms_recipe))
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"An error occurred while adding mom's recipe: {e}")
            self.conn.rollback()
            return "error"
        finally:
            cursor.close()

    def get_moms_recipe(self):
            cursor = self.conn.cursor()
            query = """
            SELECT mr.ID, u.Name AS Username, mr.MomsRecipe
            FROM momsrecipe mr
            JOIN user u ON mr.UserID = u.ID;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            momsrecipe_details = []
            for item in result:
                momsrecipe_details.append({
                    "UserID": item[0],
                    "UserName": item[1],
                    "Recipe": item[2],
                })
            return momsrecipe_details            
