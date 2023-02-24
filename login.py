from db_con import SQLConnection
import datetime
from datetime import date


class Login:

    def __init__(self, email: str, pwd: str):
        self.email = email
        self.password = pwd

    def loginCheck(self, email, password):
        sqlcon = SQLConnection()
        try:
            self.email = email
            self.password = password
            print(self.email)
            query = "select c.Email,c.Password from customer c where c.Email=%s"
            cursor = SQLConnection.cursor(sqlcon)
            cursor.execute(query, (self.email,))
            my_result = cursor.fetchall()
            print(my_result)
            if len(my_result) != 0:
                print(my_result[0][0], my_result[0][1])
                in_query = "insert into Login(Email,Password,Date) values(%s,%s,%s)"
                today = date.today()
                values = (my_result[0][0], my_result[0][1], today)
                cursor.execute(in_query, values)
                print("Logged In Successfully")
                SQLConnection.commit(sqlcon)
                flag = True
            else:
                flag = False
            return flag
        except Exception as ex:
            print(f"Exception occurred ={ex}")
        finally:
            SQLConnection.close(sqlcon)
