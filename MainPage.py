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
        
        label1 = tk.Label(self, text="ShareWithMe")
        label1.config(font=("Courier", 45, 'bold'))
        label2 = Label(self, text="AccountID")
        label3 = Label(self, text="Password")
        ###BACKEDN NEED TO VERIFY IN CORRECT PASSWORD ENTERED
        
        #ENTRIES
        entry1 = Entry(self)
        entry2 = Entry(self,show='*')
        #filename = PhotoImage(file = "/Users/Binod/Desktop/college/Fall2018/SoftwareEngineering/DocumentSharingSystem/backgroundImage.png")
        #background_label = Label(self, image=filename)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        
    
        #BUTTONS
        button1 = tk.Button(self, text="Sign Up",command=lambda: controller.show_frame("SignupPage"))
        #if you enter super as accountID and password then you will go to super page
        #this feature can be cahnged later based on the feature we want
        button2 = tk.Button(self, text="Log In",command=lambda: controller.check_show_frame(entry1,entry2,"SuperPage","OrdinaryPage"))#command=lambda: controller.show_frame("OrdinaryPage")
        button3 = tk.Button(self, text="Guest User",command=lambda: controller.show_frame("GuestPage"))
        checkbox1 = Checkbutton(self, text="Keep me Logged in", fg="black")
        ###BACKEND NEED TO CHEK IF KEEP ME LOGIN CHECKED OR NOT
        
        
        
        #CO-ORDINATES
        n = 150
        m = 50


        
        ##PLACING THE LABELS
        label_type.pack(side=BOTTOM)
        label1.pack(side=TOP,ipady=50)
        label2.place(x=n, y=m*4)
        label3.place(x=n, y=m*5)
        
        ##PLACING THE ENTRIES
        entry1.place(x=n+100, y=m*4)
        entry2.place(x=n+100, y=m*5)
        
        ##PLACING THE BUTTON
        button1.place(x=n+30,y=m*7)
        button2.place(x=n+130,y=m*7)
        button3.place(x=n+230,y=m*7)
        
        ##PLACING THE CHECKBOX
        checkbox1.place(x=n+100,y=m*6)
