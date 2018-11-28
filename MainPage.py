#############################################################################
#Name:MainPage.py
#Description: The page we see first when we run the program. We could log in,
#             sign up or exit the program in this page.
#############################################################################
import tkinter as tk
from tkinter import *

class MainPage(tk.Frame):

    #Initializer
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #This function gets called when "log in" button is clicked.
        #It checkes username and password in the file and takes the user
        #to the corresponding page depening on their user type.
        def check_user(name, password): 
            
            #Opens "user_info" which stores all the username and password info
            user_info_file = open("user_info", "r") #"r": read only
            
            #The while loop reads users' info in turn and matches usernames and passwords
            while True:
                user_id_string = user_info_file.readline()      #read user id as a string
                
                #Stop reading the file when there's no more information
                if user_id_string == '':
                    break
                
                user_id = int(user_id_string)                   #convert string into int
                user_name = user_info_file.readline()           #read user_name
                user_name = user_name.replace("\n", "")         #get rid of "\n" in user_name
                user_password = user_info_file.readline()       #read user_password
                user_password = user_password.replace("\n", "") #get rid of "\n" in user_password
                user_type = user_info_file.readline()           #read user_type
                user_type = user_type.replace("\n", "")         #get rid of "\n" in user_type
                user_info_file.readline()                       #skip *

                #If both username and password match, go to corresponding page
                if (name == user_name and password == user_password):
                    frame = controller.page_array[user_type]
                    frame.tkraise()
                    return
            
            #If no match found, show the error message
            tk.messagebox.showinfo("Login error","The username or password "\
                                        "you entered is incorrect")

        #############
        #    GUI    #
        #############
        
        #LABLES
        label_type = tk.Label(self, text="? FourOfUS 2018", fg = "gray",font=controller.footer_font)
        label = tk.Label(self, text="ShareWithMe")
        label.config(font=("Courier", 45, 'bold'))
        label_name = Label(self, text="Username")
        label_password = Label(self, text="Password")
        
        #ENTRIES
        entry_name = Entry(self)
        entry_password = Entry(self,show='*')
        
        #BUTTONS
        button_signup = tk.Button(self, text="Sign Up",command=lambda: controller.show_frame("SignupPage"))
        button_login = tk.Button(self, text="Log In",command=lambda: check_user(entry_name.get(),entry_password.get()))
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
