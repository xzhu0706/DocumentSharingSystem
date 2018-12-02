import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from OrdinaryUser import *

class SuperUser(OrdinaryUser):

    def __init__(self, parent, controller):

        super(SuperUser, self).__init__(parent, controller)

        update_membership_button = tk.Button(self, text="Manage Membership")  # ,command=lambda:TO BE IMPLEMENTED BY BACKEND, can update or remove user
        taboo_words_button = tk.Button(self, text="Taboo Words")  # ,command=lambdaTO BE IMPLEMENTED BY BACKEND

        # PLACING THE LABELS
        n = 150
        m = 50

        update_membership_button.place(x=n + 300, y=m * 8.5)
        taboo_words_button.place(x=n + 300, y=m * 9)

# class SuperUser(tk.Frame):
#
#     def __init__(self, parent, controller, userid, username):
#
#         self.userid = userid
#         self.username = username
#
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#
#         #Options for drop down just an example need to be implemented
#         OPTIONS = [
#                    "DOCUMENT 1",
#                    "DOCUMENT 2",
#                    "DOCUMENT 3"
#                    ] #etc
#         variable = StringVar(self)
#         variable.set("PLEASE SELECT A DOCUMENT")
#                    ##LABELS
#         label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
#         label1 = tk.Label(self, text="ShareWithME")
#         label1.config(font=("Courier", 35, 'bold'))
#         label2 = Label(self, text="Welcome to your Home Page, Super\n\nHere are your Documents:")
#         label2.config(font=("Courier", 20))
#
#         #DROP DOWN
#         ##REFRENE FOR DROP DOWN
#         '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
#         #doc1, doc 2 need to be replaced by the bakedn data
#         dropDown1 = OptionMenu(self, variable, *OPTIONS)
#
#
#         #BUTTONS
#         button1 = tk.Button(self, text="Open",command=lambda:controller.show_frame("DocumentPage"))
#         # NEEDED TO PULL DOCUMENT FROM BACKEND)
#
#         button2=tk.Button(self,text="Delete")#command=lambda:NEED A FUNCTION TO DELETE A SELECTED DOCUMENT FROM BACKEND
#
#         button3=tk.Button(self, fg="red",text="Create A\nNew Document ",command=lambda:controller.show_frame("DocumentPage"))
#
#
#         button4=tk.Button(self, text="Manage Invitations")#command=lambda:NEED TO CHECK FROM BACKEND IF ANYONE INVITED
#         button5=tk.Button(self, text="Log Out",fg="blue",command=lambda:controller.show_frame("MainPage"))
#
#
#         button6=tk.Button(self, text="Update Membership")#,command=lambda:TO BE IMPLEMENTED BY BACKEND
#         button7=tk.Button(self, text="Taboo Words")#,command=lambdaTO BE IMPLEMENTED BY BACKEND
#         button8=tk.Button(self, text="Process Complaints")#,command=lambda:TO BE IMPLEMENTED BY BACKEND
#
#         #PLACING THE LABELS
#         n = 150
#         m = 50
#         label_type.pack(side=BOTTOM)
#         label1.pack(side=TOP,ipady=20)
#         label2.place(x=n,y=m*3)
#
#
#         #PLACING THE DROP DOWN
#         dropDown1.place(x=n,y=m*6)
#
#         #PLACING BUTTONS
#         button1.place(x=n,y=m*7)
#         button2.place(x=n+50,y=m*7)
#
#         button3.place(x=n,y=m*9.5)
#
#         button4.place(x=n+300,y=m*10)
#         button5.place(x=n+380,y=m-20)
#
#         button6.place(x=n+300,y=m*7)
#         button7.place(x=n+300,y=m*8)
#         button8.place(x=n+300,y=m*9)
