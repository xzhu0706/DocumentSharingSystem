import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
class MainPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        #LABLES
        label_type = tk.Label(self, text="? FourOfUS 2018", fg = "gray",font=controller.footer_font)
        label = tk.Label(self, text="ShareWithMe")
        label.config(font=("Courier", 45, 'bold'))
        label_name = Label(self, text="Username")
        label_password = Label(self, text="Password")
        
        #ENTRIES
        entry_name = Entry(self)
        entry_password = Entry(self,show='*')
        #filename = PhotoImage(file = "/Users/Binod/Desktop/college/Fall2018/SoftwareEngineering/DocumentSharingSystem/backgroundImage.png")
        #background_label = Label(self, image=filename)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        #BUTTONS
        button_signup = tk.Button(self, text="Sign Up",command=lambda: controller.show_frame("SignupPage"))
        #if you enter super as accountID and password then you will go to super page
        #this feature can be cahnged later based on the feature we want
        button_login = tk.Button(self, text="Log In",command=lambda: controller.check_user(entry_name.get(),entry_password.get()))
        button_guest = tk.Button(self, text="Guest User",command=lambda: controller.show_frame("GuestPage"))
        checkbox1 = Checkbutton(self, text="Keep me Logged in", fg="black")
        
        
        
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
        checkbox1.place(x=n+100,y=m*6)
