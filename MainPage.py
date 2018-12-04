#############################################################################
#Name:MainPage.py
#Description: The page we see first when we run the program. We could log in,
#             sign up or exit the program in this page.
#############################################################################
import tkinter as tk
from tkinter import *
import pandas as pd

class MainPage(tk.Frame):

    # Constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #This function gets called when "log in" button is clicked.
        #It checkes username and password in the file and takes the user
        #to the corresponding page depening on their user type.

        def check_user(username_input, password_input):
            accounts_db = pd.read_csv("database/UserInfos.csv", delimiter=',')
            accounts_applications_db = pd.read_csv("database/PendingApplications.csv", delimiter=',')
            # print(accounts_db) ## uncomment this line to see what is in db

            # Check if all fields are filled
            if username_input == '' or password_input == '':
                tk.messagebox.showerror("Error", "Please fill out all the fields!")
                return

            # Check if username is in pending applications db
            if not accounts_applications_db.loc[accounts_applications_db['username'] == username_input].empty:
                tk.messagebox.showerror("Error", "Your application is still pending!")
                return

            # Check if username exists in db, if yes then check password
            user_info = accounts_db.loc[accounts_db['username'] == username_input]
            if user_info.empty:
                tk.messagebox.showerror("Error", "Wrong username!")
            else:
                if password_input == user_info.get('password').values[0]:
                    # If password match, set user info into the system by calling the controller method
                    username = username_input
                    userid = user_info.get('id').values[0]
                    usertype = user_info.get('usertype').values[0]
                    controller.log_in(username, userid, usertype)
                    # frame = controller.page_array[usertype]
                    # frame.tkraise()
                else:
                    tk.messagebox.showerror("Error", "Wrong password!")

        #############
        #    GUI    #
        #############
        
        #LABLES
        label_type = tk.Label(self, text="® FourOfUS 2018", fg = "gray",font=controller.footer_font)
        label = tk.Label(self, text="ShareWithMe")
        label.config(font=("Courier", 45, 'bold'))
        label_name = Label(self, text="Username")
        label_password = Label(self, text="Password")
        
        #ENTRIES
        entry_name = Entry(self)
        entry_password = Entry(self,show='*')
        
        #BUTTONS
        button_signup = tk.Button(self, text="Sign Up",command=lambda: controller.show_frame("SignupPage"))
        button_login = tk.Button(self, text="Log In",command=lambda: check_user(entry_name.get(),
                                                                                entry_password.get()))
        button_guest = tk.Button(self, text="Guest User",command=lambda: controller.show_frame("Guest"))
        #**********************
        #Need to work on this
        #**********************
        checkbox_keep_login = Checkbutton(self, text="Keep me logged in", fg="black")
        
        #CO-ORDINATES
        n = 150
        m = 50

        ##PLACING THE LABELS
        label_type.pack(side=BOTTOM)
        label.pack(side=TOP,ipady=50)
        label_name.place(x=n, y=m*4)
        label_password.place(x=n, y=m*5)
        
        ##PLACING THE ENTRIES
        entry_name.place(x=n+100, y=m*4)
        entry_password.place(x=n+100, y=m*5)
        
        ##PLACING THE BUTTON
        button_login.place(x=n+30,y=m*7)
        button_signup.place(x=n+130,y=m*7)
        button_guest.place(x=n+230,y=m*7)
        
        ##PLACING THE CHECKBOX
        checkbox_keep_login.place(x=n+100,y=m*6)