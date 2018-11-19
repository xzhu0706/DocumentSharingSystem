import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image

class SignupPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        def sign_up():
            '''This is the function called when "sign up" is clicked'''
            sign_up_file = open("user_info.txt", "r+") #"r+": read and write from the begining

            #the while loop reads and updates the users' info until it's the last user
            while True:
                user_id_string = sign_up_file.readline()
                if user_id_string == '':
                    break
                user_id = int(user_id_string)
                sign_up_file.readline() #skip user_name
                sign_up_file.readline() #skip user_password
                sign_up_file.readline() #skip user_type
                sign_up_file.readline() #skip *

            #get the info for the new user
            user_id = user_id + 1         #assign a new id to the user
            user_name = entry_name.get()      #get the user_name
            user_password = entry_password.get()  #get the user_password
            user_type = "ou"              #get the user_type

            #writes all the info into the file
            print(user_id, file=sign_up_file)
            print(user_name, file=sign_up_file)
            print(user_password, file=sign_up_file)
            print(user_type, file=sign_up_file)
            print('*', file=sign_up_file)
            sign_up_file.close()
            messagebox.showinfo("Information","Account Created, Please Login!!") #show messagebox after signup
            controller.show_frame("MainPage")   #go back to home page
            #end of sign_up()

        
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
        
        #ENTRIES
        entry_name = Entry(self)
        entry_email = Entry(self)
        entry_phone = Entry(self)
        entry_password = Entry(self,show='*')

        #BUTTONS
        button_back = tk.Button(self, text="Back",command=lambda:controller.show_frame("MainPage"))
        button_signup = tk.Button(self, text="Sign UP",
                            command=sign_up)
    
        n = 150
        m = 25
        
        ##PLACING THE LABELS
        label_type.pack(side = BOTTOM)
        label.pack(side=TOP,ipady=20)
        label_name.place(x=n, y=m*5)
        label_email.place(x=n, y=m*7)
        label_phone.place(x=n, y=m*9)
        label_password.place(x=n, y=m*11)
        
        ##PLACING THE ENTRIES
        entry_name.place(x=n+125, y=m*5)
        entry_email.place(x=n+125, y=m*7)
        entry_phone.place(x=n+125, y=m*9)
        entry_password.place(x=n+125, y=m*11)
        
        ##PLACING THE BUTTONS
        button_back.place(x=150,y=350)
        button_signup.place(x=250,y=350)

        
        

            
