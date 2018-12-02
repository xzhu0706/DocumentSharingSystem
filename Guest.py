import tkinter as tk
from tkinter import *

class Guest(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.ID="guest"
        #Options for drop down just an example
        #need all documents for guest
        OPTIONS = [
                   "DOCUMENT 1",
                   "DOCUMENT 2",
                   "DOCUMENT 3"
                   ] #etc
            
        variable = StringVar(self)
        variable.set("PLEASE SELECT A DOCUMENT")
                   ##LABELS
        label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
        label1 = tk.Label(self, text="ShareWithME")
        label1.config(font=("Courier", 35, 'bold'))
        label2 = Label(self, text="Welcome to your Home Page, {}!\nSelect a document:".format(controller.get_username()))
        label2.config(font=("Courier", 20))
                   
        #DROP DOWN
        ##REFRENE FOR DROP DOWN
        '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
        #doc1, doc 2 need to be replaced by the bakend data
        dropDown1 = OptionMenu(self, variable, *OPTIONS)
                   
                   
        #BUTTONS
        open_doc_button = tk.Button(self,text="Open",command=lambda:controller.show_frame("DocumentPage"))
        # NEEDED TO PULL THE SELECTED DOCUMENT FROM BACKEND)

        back_button = tk.Button(self,text="Back",command=lambda:controller.show_frame("MainPage"))

        suggest_taboo_button = tk.Button(self,text="Suggest Taboo Words")#, command=lambda:)
                   
                   
                  
        #PLACING THE LABELS
        n = 150
        m = 50
        label_type.pack(side=BOTTOM)
        label1.pack(side=TOP,ipady=20)
        label2.place(x=n-50,y=m*3)
                   
                   
        #PLACING THE DROP DOWN
        dropDown1.place(x=n-50,y=m*6)
                   
        #PLACING BUTTONS
        open_doc_button.place(x=n-50,y=m*7)
        back_button.place(x=n+50, y=m*7)
        suggest_taboo_button.place(x=n+300, y=m*10.5)

    #def open_doc(self, ):