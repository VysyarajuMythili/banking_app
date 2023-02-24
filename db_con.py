import mysql.connector


class SQLConnection:

    def __init__(self):
        self.con = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Mytiraju@2302',
            database='test',
            port='3306',

        )
        self.cursor = self.con.cursor()

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()

    def cursor(self):
        return self.cursor

    def connection(self):
        return self.con
