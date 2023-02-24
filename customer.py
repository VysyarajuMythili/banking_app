from db_con import SQLConnection


class Customer:

    def __init__(self, nm: str, age: int, mobile_num: str, mail_id: str,
                 dob: str, aadhar_no: str, pan_no: str, pwd: str):
        self.name = nm
        self.age = age
        self.mobile_no = mobile_num
        self.mail = mail_id
        self.date_of_birth = dob
        self.aadhar_num = aadhar_no
        self.pan_num = pan_no
        self.password = pwd

    def ins_record(self):
        sqlcon = SQLConnection()
        try:
            ins_query = "insert into Customer(Name,Age,Mobile_no,Email,Date_of_birth," \
                        "Aadhar_number,Pan_number,Password)" \
                        "values(%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (self.name, self.age, self.mobile_no, self.mail, self.date_of_birth, self.aadhar_num,
                   self.pan_num, self.password)
            cursor = SQLConnection.cursor(sqlcon)
            cursor.execute(ins_query, val)
            SQLConnection.commit(sqlcon)

        except Exception as ex:
            print(f"Exception occurred ={ex}")
        SQLConnection.close(sqlcon)
