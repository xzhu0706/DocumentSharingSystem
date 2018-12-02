import pandas as pd
import tkinter as tk
from tkinter import *

class SignupPage(tk.Frame):
    
    def __init__(self, parent, controller):

        def sign_up(user_name, user_password, tech_interest):
            '''This is the function called when "sign up" is clicked'''

            # get exisiting usernames from db to prevent duplicates
            applications_db = pd.read_csv("database/PendingApplications.csv", delimiter=',')
            accounts_db = pd.read_csv("database/UserInfos.csv", delimiter=',')
            existing_pending_usernames = applications_db['username'].values.tolist()
            existing_usernames = accounts_db['username'].values.tolist()

            # Check if all fields are filled
            if user_name == '' or user_password == '' or tech_interest == '':
                tk.messagebox.showerror("", "Please fill out all the fields!")
                return

            # Check if username already existed in pending applications
            if existing_pending_usernames:
                for username in existing_pending_usernames:
                    if user_name == username:
                        tk.messagebox.showerror("Error", "You application is still pending, please wait for approval!")
                        return

            # Check if username already existed in accounts db
            if existing_usernames:
                for username in existing_usernames:
                    if user_name == username:
                        tk.messagebox.showerror("Error", "User name already existed, please re-enter!")
                        return

            # Add account application to db
            data = [[user_name, user_password, tech_interest]]
            df = pd.DataFrame(data, columns=['username', 'password', 'technical_interest'])
            with open('database/PendingApplications.csv', 'a') as pending_applications_db:
                df.to_csv(pending_applications_db, index=False, header=False)
            tk.messagebox.showinfo("Information", "Registration is successful, please wait for approval.")
            controller.show_frame("MainPage")

        
        # def sign_up():
        #     '''This is the function called when "sign up" is clicked'''
        #     sign_up_file = open("user_info", "r+") #"r+": read and write from the begining
        #
        #     #the while loop reads and updates the users' info until it's the last user
        #     while True:
        #         user_id_string = sign_up_file.readline()
        #         if user_id_string == '':
        #             break
        #         user_id = int(user_id_string)
        #         sign_up_file.readline() #skip user_name
        #         sign_up_file.readline() #skip user_password
        #         sign_up_file.readline() #skip user_type
        #         sign_up_file.readline() #skip *
        #
        #     #get the info for the new user
        #     user_id = user_id + 1         #assign a new id to the user
        #     user_name = entry_name.get()      #get the user_name
        #     user_password = entry_password.get()  #get the user_password
        #     user_type = "OrdinaryUser"              #get the user_type
        #
        #     #writes all the info into the file
        #     print(user_id, file=sign_up_file)
        #     print(user_name, file=sign_up_file)
        #     print(user_password, file=sign_up_file)
        #     print(user_type, file=sign_up_file)
        #     print('*', file=sign_up_file)
        #     sign_up_file.close()
        #
        #     #clear the entries
        #     entry_name.delete(0, END)
        #     entry_email.delete(0, END)
        #     entry_phone.delete(0, END)
        #     entry_password.delete(0, END)
        #
        #     tk.messagebox.showinfo("Information","Account Created, Please Login!!") #show messagebox after signup
        #     controller.show_frame("MainPage")   #go back to home page
        #     #end of sign_up()

        
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        #LABELS
        label_type = tk.Label(self, text="® FourOfUS 2018", fg = "gray",font=controller.footer_font)
        label = tk.Label(self, text="ShareWithMe")
        label.config(font=("Courier", 35, 'bold'))
        label_name = tk.Label(self, text="Name")
        label_email = tk.Label(self, text="Email")
        label_phone = tk.Label(self, text="Phone Number")
        label_password = tk.Label(self, text="Password")
        label_tech_interest = tk.Label(self, text="Technical Interest")
        
        #ENTRIES
        entry_name = Entry(self)
        entry_email = Entry(self)
        entry_phone = Entry(self)
        entry_password = Entry(self,show='*')
        entry_tech_interest = Entry(self)

        #BUTTONS
        button_back = tk.Button(self, text="Back",command=lambda:controller.show_frame("MainPage"))
        button_signup = tk.Button(self, text="Sign Up",
                            command=lambda: sign_up(entry_name.get(),
                                                    entry_password.get(),
                                                    entry_tech_interest.get()))
    
        n = 150
        m = 25
        
        ##PLACING THE LABELS
        label_type.pack(side = BOTTOM)
        label.pack(side=TOP,ipady=20)
        label_name.place(x=n, y=m*5)
        label_email.place(x=n, y=m*7)
        label_phone.place(x=n, y=m*9)
        label_password.place(x=n, y=m*11)
        label_tech_interest.place(x=n, y=m*13)
        
        ##PLACING THE ENTRIES
        entry_name.place(x=n+125, y=m*5)
        entry_email.place(x=n+125, y=m*7)
        entry_phone.place(x=n+125, y=m*9)
        entry_password.place(x=n+125, y=m*11)
        entry_tech_interest.place(x=n+125, y=m*13)
        
        ##PLACING THE BUTTONS
        button_back.place(x=250,y=380)
        button_signup.place(x=350,y=380)

        
        

            
