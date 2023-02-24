import tkinter
import tkinter as tk
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from tkinter import messagebox, CENTER
import login as lo
import customer as cu
import smtplib
import Account as ac
from fpdf import FPDF, XPos, YPos

root = tk.Tk()
root.title("Chatbot")
root.geometry("800x800")
BG_COLOR = "#4CAF50"
TEXT_COLOR = "#EAECEE"
TXT_COLOR = "#333333"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def displayBalance(mail_id):
    ac_obj = ac.Account(mail_id)
    balance = ac_obj.getBalance(mail_id)
    print(balance)
    scr = tk.Tk()
    scr.geometry("800x800")
    scr.title("Balance Page")
    my_text = tk.Entry(scr, justify=CENTER, font=FONT, fg=TEXT_COLOR)
    txt = "Balance:" + str(balance)
    my_text.insert(0, txt)
    my_text.pack(padx=50, pady=50)


def addingAmt(mail, acc, amt):
    print(f"{amt} to be deposited for the account :{acc}")
    try:
        ac_obj = ac.Account(mail)
        ac_obj.deposit(acc, amt)
    except Exception as ex:
        print(f"Exception = {ex}")


def depositAmt(mail):
    w_screen = tk.Tk()
    w_screen.geometry("800x800")
    w_screen.title("DEPOSIT PAGE")
    acc_lbl = tk.Label(w_screen, text='Account No:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    acc_lbl.grid(row=1, column=0, padx=5, pady=5)

    acc_ent = tk.Entry(w_screen, font=FONT, fg=TXT_COLOR)
    acc_ent.grid(row=1, column=1, padx=5, pady=5)

    amt_lbl = tk.Label(w_screen, text='Amount:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    amt_lbl.grid(row=2, column=0, padx=5, pady=5)

    amt_ent = tk.Entry(w_screen, font=FONT, fg=TXT_COLOR)
    amt_ent.grid(row=2, column=1, padx=5, pady=5)

    submit = tk.Button(w_screen, text="SUBMIT", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR,
                       command=lambda: addingAmt(mail, acc_ent.get(), float(amt_ent.get())))
    submit.grid(row=3, column=0, padx=5, pady=5)


def validate(mail, pd):
    print(f"The name entered by you is {mail} {pd}")
    try:
        obj = lo.Login(mail, pd)
        res = obj.loginCheck(mail, pd)
        if res:
            messagebox.showinfo('Success', 'Logged successfully')
            screen = tk.Tk()
            screen.geometry("800x800")
            screen.title("Banking options")
            button3 = tk.Button(screen, text="Issue DD", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR,
                                command=lambda: issueDD(mail))
            button3.grid(row=1, column=0, padx=130, pady=10)
            button4 = tk.Button(screen, text="Check Balance", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR,
                                command=lambda: displayBalance(mail))
            button4.grid(row=1, column=1, padx=150, pady=10)
            button5 = tk.Button(screen, text="Deposit", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR,
                                command=lambda: depositAmt(mail))
            button5.grid(row=1, column=2, padx=150, pady=10)
        elif not res:
            messagebox.showinfo('Login Failed', 'email_id and password mismatch')
    except Exception as ex:
        print(f"Exception = {ex}")


def account(name, age, mobile, mail, dob, aadhar, pan, pwd):
    obj = cu.Customer(name, age, mobile, mail, dob, aadhar, pan, pwd)
    obj.ins_record()


def generate_pdf(name, acc_no):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=15)
    value = "Name:" + name + "\n" + "Account Number:" + str(acc_no)
    pdf.cell(200, 10, txt=value,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.output("sample.pdf")


def generate_dd(email, name, amount, date):
    ac_obj = ac.Account(email)
    bal = ac_obj.getBalance(email)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=15)
    value = "Issued in favour of :" + name + "\n" + "Amount:" + str(amount) + "\n" + "issued date:" + str(
        date) + '\n' + "Available Balance:" + str(bal)
    pdf.cell(200, 10, txt=value,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.output("DD_acknowledgement.pdf")
    messagebox.showinfo('Success', 'DD is generated.please collect it from registered branch')
    sender = "mythilivysyaraju@gmail.com"
    receiver_mail = email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver_mail
    msg['Subject'] = "DD ACKNOWLEDGEMENT"
    body = "Here is the attached file with DD details."
    msg.attach(MIMEText(body, 'plain'))
    filename = "sample.pdf"
    attachment = open("E:/PythonWorkspace/SBIProject/DD_acknowledgement.pdf", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("mythilivysyaraju@gmail.com", "lqtjbuqwuivxsdgs")
        text = msg.as_string()
        s.sendmail("mythilivysyaraju@gmail.com", receiver_mail, text)
        s.quit()
    except Exception as e:
        print(e)


def issueDD(email):
    w_screen = tk.Tk()
    w_screen.geometry("800x800")
    w_screen.title("Issue DD PAGE")
    name_lbl = tk.Label(w_screen, text='Issue in favour of:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    name_lbl.grid(row=1, column=0, padx=5, pady=5)

    name_ent = tk.Entry(w_screen, font=FONT, fg=TXT_COLOR)
    name_ent.grid(row=1, column=1, padx=5, pady=5)

    amt_lbl = tk.Label(w_screen, text='Amount:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    amt_lbl.grid(row=2, column=0, padx=5, pady=5)

    amt_ent = tk.Entry(w_screen, font=FONT, fg=TXT_COLOR)
    amt_ent.grid(row=2, column=1, padx=5, pady=5)

    dd_lbl = tk.Label(w_screen, text='Date of Issue:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    dd_lbl.grid(row=3, column=0, padx=5, pady=5)

    dd_ent = tk.Entry(w_screen, font=FONT, fg=TXT_COLOR)
    dd_ent.grid(row=3, column=1, padx=5, pady=5)

    submit = tk.Button(w_screen, text="Generate DD", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR,
                       command=lambda: generate_dd(email, name_ent, amt_ent, dd_ent))
    submit.grid(row=4, column=0, padx=5, pady=5)


def login():
    screen = tk.Tk()
    screen.geometry("800x800")
    screen.title(" Login Page")
    email_lbl = tk.Label(screen, text='Email:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    email_lbl.grid(row=1, column=0, padx=5, pady=5)

    email_ent = tk.Entry(screen, font=FONT, fg=TXT_COLOR)
    email_ent.grid(row=1, column=1, padx=5, pady=5)

    pwd_lbl = tk.Label(screen, text='Password:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    pwd_lbl.grid(row=2, column=0, padx=5, pady=5)

    pwd_ent = tk.Entry(screen, font=FONT, fg=TXT_COLOR)
    pwd_ent.grid(row=2, column=1, padx=5, pady=5)

    submit = tk.Button(screen, text="SUBMIT", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR,
                       command=lambda: validate(email_ent.get(), pwd_ent.get()))
    submit.grid(row=3, column=0, padx=5, pady=5)

    clear = tk.Button(screen, text="CLEAR", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR)
    clear.grid(row=3, column=1, padx=5, pady=5)


def send_email(name, email):
    ac_obj = ac.Account(email)
    acc_num = ac_obj.createAccount()
    generate_pdf(name, acc_num)
    sender = "mythilivysyaraju@gmail.com"
    receiver_mail = email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver_mail
    msg['Subject'] = "Account details"
    body = "Here is the attached file with account details."
    msg.attach(MIMEText(body, 'plain'))
    filename = "sample.pdf"
    attachment = open("E:/PythonWorkspace/SBIProject/sample.pdf", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("mythilivysyaraju@gmail.com", "lqtjbuqwuivxsdgs")
        text = msg.as_string()
        s.sendmail("mythilivysyaraju@gmail.com", receiver_mail, text)
        s.quit()
    except Exception as e:
        print(e)


def register():
    reg_screen = tk.Tk()
    reg_screen.geometry("800x800")
    reg_screen.title("Registration")
    name_lbl = tk.Label(reg_screen, text='Name:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    name_lbl.grid(row=1, column=0, padx=5, pady=5)

    name_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    name_ent.grid(row=1, column=1, padx=5, pady=5)

    age_lbl = tk.Label(reg_screen, text='Age:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    age_lbl.grid(row=2, column=0, padx=5, pady=5)

    age_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    age_ent.grid(row=2, column=1, padx=5, pady=5)

    mobile_lbl = tk.Label(reg_screen, text='Mobile:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    mobile_lbl.grid(row=3, column=0, padx=5, pady=5)

    mobile_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    mobile_ent.grid(row=3, column=1, padx=5, pady=5)

    mail_lbl = tk.Label(reg_screen, text='Email:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    mail_lbl.grid(row=4, column=0, padx=5, pady=5)

    mail_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    mail_ent.grid(row=4, column=1, padx=5, pady=5)

    dob_lbl = tk.Label(reg_screen, text='DateOfBirth:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    dob_lbl.grid(row=5, column=0, padx=5, pady=5)

    dob_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    dob_ent.grid(row=5, column=1, padx=5, pady=5)

    aadhar_lbl = tk.Label(reg_screen, text='Aadhar Number:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    aadhar_lbl.grid(row=6, column=0, padx=5, pady=5)

    aadhar_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    aadhar_ent.grid(row=6, column=1, padx=5, pady=5)

    pan_lbl = tk.Label(reg_screen, text='PAN Number:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    pan_lbl.grid(row=7, column=0, padx=5, pady=5)

    pan_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    pan_ent.grid(row=7, column=1, padx=5, pady=5)

    pwd_lbl = tk.Label(reg_screen, text='create Password:', font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    pwd_lbl.grid(row=8, column=0, padx=5, pady=5)

    pwd_ent = tk.Entry(reg_screen, font=FONT, fg=TXT_COLOR)
    pwd_ent.grid(row=8, column=1, padx=5, pady=5)

    create_Account = tk.Button(reg_screen, text="CREATE ACCOUNT", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR,
                               command=lambda: [account(name_ent.get(), age_ent.get(), mobile_ent.get(),
                                                        mail_ent.get(), dob_ent.get(),
                                                        aadhar_ent.get(), pan_ent.get(), pwd_ent.get()),
                                                send_email(name_ent.get(), mail_ent.get())])
    create_Account.grid(row=9, column=0, padx=5, pady=5)

    button = tk.Button(reg_screen, text="Close", font=FONT_BOLD, bg=BG_COLOR, fg=TEXT_COLOR, command=reg_screen.destroy)
    button.grid(row=9, column=1, padx=5, pady=5)


top_frame = tk.Frame(root)
top_frame.place(x=5, y=5, width=1440, height=100)
top_title = tk.Label(top_frame, text='Welcome to SBI', font=(FONT_BOLD, 24))
top_title.pack(pady=10)
button1 = tk.Button(top_frame, text="SIGN UP", font=FONT_BOLD, bg=BG_COLOR,
                    fg=TEXT_COLOR, width=6, height=6, command=lambda: register())
button1.pack(side=tkinter.RIGHT, padx=80)
button2 = tk.Button(top_frame, text="LOGIN", font=FONT_BOLD, bg=BG_COLOR,
                    fg=TEXT_COLOR, width=6, height=6, command=lambda: login())
button2.pack(side=tkinter.RIGHT, padx=75)

root.mainloop()
