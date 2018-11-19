import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
class GuestPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.ID="guest"
        #Options for drop down just an example
        #need all documents for guest
        OPTIONS = [
                   "DOCUMENT 1",
                   "DOCUMENT 2",
                   "DOCUMENT 3",
                   "DOCUMENT 4",
                   "DOCUMENT 5"
                   ] #etc
            
        variable = StringVar(self)
        variable.set("PLEASE SELECT A DOCUMENT")
                   ##LABELS
        label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
        label1 = tk.Label(self, text="ShareWithME")
        label1.config(font=("Courier", 35, 'bold'))
        label2 = Label(self, text="Welcome to the Home Page, Guest\nSelect a document you want to view:")
        label2.config(font=("Courier", 20))
                   
        #DROP DOWN
        ##REFRENE FOR DROP DOWN
        '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
        #doc1, doc 2 need to be replaced by the bakend data
        dropDown1 = OptionMenu(self, variable, *OPTIONS)
                   
                   
        #BUTTONS
        button1 = tk.Button(self,text="Open",command=lambda:controller.show_frame("DocumentPage"))
        # NEEDED TO PULL THE SELECTED DOCUMENT FROM BACKEND)

        button2 = tk.Button(self,text="Back",command=lambda:controller.show_frame("MainPage"))
                   
                   
                  
        #PLACING THE LABELS
        n = 150
        m = 50
        label_type.pack(side=BOTTOM)
        label1.pack(side=TOP,ipady=20)
        label2.place(x=n-50,y=m*3)
                   
                   
        #PLACING THE DROP DOWN
        dropDown1.place(x=n-50,y=m*6)
                   
        #PLACING BUTTONS
        button1.place(x=n-50,y=m*7)
        button2.place(x=n+50, y=m*7)
