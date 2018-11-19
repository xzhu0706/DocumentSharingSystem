import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
class DocumentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
        label1 = tk.Label(self, text="ShareWithME")
        label1.config(font=("Courier", 35, 'bold'))
        T = Text(self,height=32, width=60,highlightbackground="black", highlightcolor="black", highlightthickness=1)
        #need to save everythin in it lets after 10 sec
        #T.insert(CURRENT,"HellO")
        
        n = 150
        m = 50
        
        button1 = tk.Button(self,text="Save")#,command=lambda:)
        button2 = tk.Button(self,text="Lock")#,command=lambda:)
        
        button3 = tk.Button(self,text="Add Contributors" )#,command=lambda:)
        button4=tk.Button(self, text="Log Out",fg="blue",command=lambda:controller.show_frame("MainPage"))
        
        #or now neeed to change the implementation it should go to super or ordinary or guest
        button5 = tk.Button(self,text="Back",command=lambda:controller.show_frame("MainPage"))
        
        button6 = tk.Button(self,text="Complain")#,command=lambda:)
        button7 = tk.Button(self,text="Taboo Words")#,command=lambda:)
        
    


        label_type.pack(side=BOTTOM)
        label1.pack(side=TOP,ipady=20)
        T.place(x=n-120,y=m+20)
        
        button1.place(x=n+325, y=m*3)
        button2.place(x=n+325, y=m*4)
        button3.place(x=n+325, y=m*5)
        button4.place(x=n+380,y=m-20)
        button5.place(x=n+325, y=m*6)
        button6.place(x=n+325, y=m*7)
        button7.place(x=n+325, y=m*8)
