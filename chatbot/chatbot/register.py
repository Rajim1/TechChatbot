from tkinter import*
from tkinter import messagebox
import sqlite3
import re
import subprocess
from numpy import var

f = ('Times', 14)

con2 = sqlite3.connect('userdata2.db')
cur = con2.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
            "ID"	INTEGER NOT NULL,
            "Name"	TEXT NOT NULL,
	        "Contact"	INTEGER NOT NULL UNIQUE,
            "Password"  TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT)
            )
        ''')
        
con2.commit()
 
ws = Tk()
ws.title ('Registration')
ws.geometry('1000x500')
ws.config(bg='#0B5A81')
ws.iconbitmap('C:\\Project\\chatbot\\chatbot')
#def run_program():
#    ws.destroy()
#    subprocess.call(["python", "chatgui.py"])



#For registration
def insert_record():
    check_counter=0
    warn = ""
    if register_name.get() == "":
        warn = "Name can't be empty"
    else:
        check_counter +=1
    if register_contact.get() == "":
            warn = "Contact can't be empty"
    else:
        check_counter +=1
    if register_pwd.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter +=1
    if pwd_again.get() =="":
        warn = "Re-enter password can't be empty"
    else: 
        check_counter +=1
    if register_pwd.get() != pwd_again.get():
        warn = "Password didn't match! Try again"
    else:
        check_counter+=1
    if check_counter >=5:
        try:
    
            con = sqlite3.connect('userdata2.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record (Name, Contact, Password) VALUES (:name, :contact, :password)", {
                        'name': register_name.get(),
                        'contact': register_contact.get(),
                        'password': register_pwd.get()
            })
            con.commit()
            messagebox.showinfo('confirmation','Record Saved!')
            
            #base.mainloop()
            
        except Exception as ep:
            messagebox.showerror('Error',ep)
    else:
        messagebox.showerror('Error',warn)

#for Login
#def login_response():
def run_program():
    ucontact = contact_tf.get()
    upwd = pwd_tf.get()
    try:
        con = sqlite3.connect('userdata2.db')
        c = con.cursor()
        for row in c.execute("Select * from record"):
            print(row)
            contact = row[2]
            pwd = row[3]
            if(ucontact == str(contact) and upwd == pwd):
                print('true')
                break
        
    except Exception as ep:
        messagebox.showerror('',ep)

    check_counter=0
    if ucontact == "":
        warn = "Contact can't be empty"
    else:
        check_counter = check_counter+1
    if upwd == "":
        warn = "Password can't be empty"
    else:
        check_counter = check_counter+1
    if check_counter ==2:
        if (ucontact == str(contact) and upwd == pwd):
            messagebox.showinfo('Login Status', 'Logged in Successfully!')
            ws.destroy()
            subprocess.call(["python", "C:\\Project\\chatbot\\chatbot\\chatgui.py"])
        
        else:
            messagebox.showinfo('Login Status', 'Invalid Contact or Password!')
    else:
        messagebox.showerror('',warn)
            
#var = StringVar()


#widgets
#Left_frame elements
left_frame = Frame(
    ws,
    bd=2,
    bg='#CCCCCC',
    relief=SOLID,
    padx=10,
    pady=10
)
#phone
Label(
    left_frame,
    text="Enter Phone",
    bg='#CCCCCC',
    font=f
    ).grid(row=0, column=0, sticky=W, pady=10)
#password
Label(
    left_frame,
    text="Enter Password",
    bg='#CCCCCC',
    font=f
    ).grid(row=1, column=0, sticky=W, pady=10)

contact_tf = Entry(
    left_frame,
    font=f
)
pwd_tf = Entry(
    left_frame,
    font=f,
    show='*'
)
login_btn = Button(
    left_frame,
    width=15,
    text='Login',
    font=f,
    relief=SOLID,
    cursor='hand2',
    command=run_program
)

#Right_frame elements
right_frame = Frame(
    ws,
    bd=2,
    bg= '#CCCCCC',
    relief=SOLID,
    padx=10,
    pady=10
)

Label(
    right_frame,
    text="Enter Name",
    bg='#CCCCCC',
    font=f
).grid(row=0, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Enter Phone",
    bg='#CCCCCC',
    font=f
).grid(row=1, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Enter Password", 
    bg='#CCCCCC',
    font=f
    ).grid(row=2, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Re-Enter Password", 
    bg='#CCCCCC',
    font=f
    ).grid(row=3, column=0, sticky=W, pady=10)


register_name = Entry(
    right_frame,
    font=f
)

register_contact = Entry(
    right_frame,
    font=f
)

register_pwd = Entry(
    right_frame,
    font=f,
    show='*'
)
pwd_again = Entry(
    right_frame,
    font=f,
    show='*'
)

register_btn=Button(
    right_frame,
    width=15,
    text='Register',
    font=f,
    relief=SOLID,
    cursor='hand2',
    command=insert_record
)

#widget_placement
#Login placement
contact_tf.grid(row=0, column=1, pady=10, padx=20)
pwd_tf.grid(row=1, column=1, pady=10, padx=20)
login_btn.grid(row=2, column=1, pady=10, padx=20)
left_frame.place(x=50, y=50)

#Register placement
register_name.grid(row=0, column=1, pady=10, padx=20)
register_contact.grid(row=1, column=1, pady=10, padx=20)
register_pwd.grid(row=2, column=1, pady=10, padx=20)
pwd_again.grid(row=3,column=1, pady=10, padx=20)
register_btn.grid(row=5, column=1, pady=10, padx=20)
right_frame.place(x=500, y=60)

ws.mainloop()
