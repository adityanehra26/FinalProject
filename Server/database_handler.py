import mysql.connector

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

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

    def close(self):
        if self.conn:
            self.conn.close()
