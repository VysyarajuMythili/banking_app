import random
from db_con import SQLConnection


class Account:

    def __init__(self, email):
        self.email_id = email
        self.balance = 0.0

    def createAccount(self):
        sqlcon = SQLConnection()
        print(sqlcon)
        try:
            print("--------- ACCOUNT CREATION ----------\n")
            account_num = random.randint(1000000000, 9999999999)
            print(f"Account created Successfully with account number={account_num}")
            ins_query = "insert into Account(Email,Account_no,Balance)" \
                        "values(%s,%s,%s)"
            val = (self.email_id, account_num, self.balance)
            cur = SQLConnection.cursor(sqlcon)
            cur.execute(ins_query, val)
            SQLConnection.commit(sqlcon)
            print(f"Account created = {account_num}")
            return account_num
        except Exception as ex:
            print(f"Exception occurred during creation of Account ={ex}")
        finally:
            SQLConnection.close(sqlcon)

    def deposit(self, acc_num, amount):
        sqlcon = SQLConnection()
        try:
            self.balance += amount
            #update_query = "update account set Balance=%s" % self.balance, "where Account_no = %s" % acc_num
            update_query = "update account set Balance=%s where Account_no = %s"
            cursor = SQLConnection.cursor(sqlcon)
            cursor.execute(update_query, (self.balance, acc_num))
            SQLConnection.commit(sqlcon)
        except Exception as ex:
            print(f"Exception occurred during deposit={ex}")
        finally:
            SQLConnection.close(sqlcon)

    def getBalance(self, email):
        self.email_id = email
        sqlcon = SQLConnection()
        try:
            sel_query = "select Balance from account where Email =%s"
            cursor = SQLConnection.cursor(sqlcon)
            cursor.execute(sel_query, (self.email_id,))
            my_result = cursor.fetchall()
            print(my_result)
            if len(my_result) != 0:
                print(my_result[0][0])
                bal = my_result[0][0]
                SQLConnection.commit(sqlcon)
            return bal
        except Exception as ex:
            print(f"Exception occurred during balance={ex}")
        finally:
            SQLConnection.close(sqlcon)






