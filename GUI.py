import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image

# Global Variables
window_dimensions = "600x600"
app_name = "Document Sharing System"

class Application(tk.Tk):
# Constructor
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(app_name)
        self.geometry(window_dimensions)
        self.resizable(0,0)
        self.title_font = font.Font(family='Courier', size=32, weight="bold", underline=True)
        self.footer_font = font.Font(family='Comic Sans MS', size=12, weight='bold',slant="italic")
        self.subheader_font = font.Font(family='Times', size=12, weight='bold',underline=True)
        # the container is where we'll stack a bunch of frames on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.page_array = {}
        
        # Classes array
        data =[MainPage,SignupPage,OrdinaryPage,GuestPage,SuperPage]
        #DocumentPage]
        
        for page in data:
            page_name = page.__name__
            current_page = page(parent=container, controller=self)
            
            self.page_array[page_name] = current_page
            
            # put all of the pages in the same location; the one on the TOP of the stacking order --> visible.
            current_page.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MainPage")
    def show_frame(self, page_name, ):
        frame = self.page_array[page_name]
        frame.tkraise()
    def check_show_frame(self, entry1,entry2,page_name1,page_name2 ):
        if(entry1.get()=="super" and entry2.get()=="super"):
            frame = self.page_array[page_name1]
            frame.tkraise()
        else:
            frame = self.page_array[page_name2]
            frame.tkraise()



class MainPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Labels
        label_type = tk.Label(self, text="® FourOfUS 2018", fg = "gray",font=controller.footer_font)
        
        label1 = tk.Label(self, text="ShareWithMe")
        label1.config(font=("Courier", 45, 'bold'))
        label2 = Label(self, text="AccountID")
        label3 = Label(self, text="Password")
        ###BACKEDN NEED TO VERIFY IN CORRECT PASSWORD ENTERED
        
        #ENTRIES
        entry1 = Entry(self)
        entry2 = Entry(self,show='*')
        
        
    
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


class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        # Labels
        label_type = tk.Label(self, text="® FourOfUS 2018", fg = "gray",font=controller.footer_font)
        label1 = tk.Label(self, text="ShareWithMe")
        label1.config(font=("Courier", 35, 'bold'))
        label2 = tk.Label(self, text="Name")
        label3 = tk.Label(self, text="Email")
        label4 = tk.Label(self, text="Phone Number")
        label5 = tk.Label(self, text="Password")
        
        
        # Entries
        entry1 = Entry(self)
        entry2 = Entry(self)
        entry3 = Entry(self)
        entry4 = Entry(self,show='*')

        
        
        
        
        # Button
        #controller.show_frame("MainPage")
        button1 = tk.Button(self, text="Home",command=lambda:controller.show_frame("MainPage"))
        ##BACKEND NEEDED FOR BUTTON 2 TO STORE DATA IN TEXT
        ##BACKEND NEEDED FOR BUTTON 2 TO STORE DATA IN TEXT
        ##BACKEND NEEDED FOR BUTTON 2 TO STORE DATA IN TEXT
        ##NEED TO CLEAR THE TEXT FIELD AFTER ACCOUNT IS CREATED
        button2 = tk.Button(self, text="Sign UP",command=lambda: messagebox.showinfo("Information","Account Created, Please Login!!"))###Back end to enforce
        button3 = tk.Button(self, text="Log IN",command=lambda: controller.show_frame("MainPage"))

        button4 = tk.Button(self, text="Exit",command=lambda: controller.destroy())
        
        n = 150
        m = 25
        ##PLACING THE LABELS
        label_type.pack(side = BOTTOM)
        label1.pack(side=TOP,ipady=20)
        label2.place(x=n, y=m*5)
        label3.place(x=n, y=m*7)
        label4.place(x=n, y=m*9)
        label5.place(x=n, y=m*11)
        
        ##PLACING THE ENTRIES
        entry1.place(x=n+125, y=m*5)
        entry2.place(x=n+125, y=m*7)
        entry3.place(x=n+125, y=m*9)
        entry4.place(x=n+125, y=m*11)
        
        ##PLACING THE BUTTONS
        button1.place(x=150,y=350)
        button2.place(x=250,y=350)
        button3.place(x=350,y=350)
        button4.place(x=450,y=350)

class SuperPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #Options for drop down just an example need to be implemented
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
        label2 = Label(self, text="Welcome to you Home Page, Super\n\nHere are your Documents:")
        label2.config(font=("Courier", 20))
       
        #DROP DOWN
        ##REFRENE FOR DROP DOWN
        '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
        #doc1, doc 2 need to be replaced by the bakedn data
        dropDown1 = OptionMenu(self, variable, *OPTIONS)
       
       
        #BUTTONS
        button1 = tk.Button(self, text="Open",command=lambda:controller.show_frame("DocumentPage"))
        # NEEDED TO PULL DOCUMENT FROM BACKEND)
       
        button2=tk.Button(self,text="Delete")#command=lambda:NEED A FUNCTION TO DELETE A SELECTED DOCUMENT FROM BACKEND
       
        button3=tk.Button(self, fg="red",text="Create A\nNew Document ",command=lambda:controller.show_frame("DocumentPage"))
       
       
        button4=tk.Button(self, text="Manage Invitations")#command=lambda:NEED TO CHECK FROM BACKEND IF ANYONE INVITED
        button5=tk.Button(self, text="Log Out",fg="blue",command=lambda:controller.show_frame("MainPage"))


        button6=tk.Button(self, text="Update Membership")#,command=lambda:TO BE IMPLEMENTED BY BACKEND
        button7=tk.Button(self, text="Lock/Unlock")#,command=lambda:TO BE IMPLEMENTED BY BACKEND
        button8=tk.Button(self, text="Taboo Words")#,command=lambdaTO BE IMPLEMENTED BY BACKEND
        button9=tk.Button(self, text="Process Complaints")#,command=lambda:TO BE IMPLEMENTED BY BACKEND
       
        #PLACING THE LABELS
        n = 150
        m = 50
        label_type.pack(side=BOTTOM)
        label1.pack(side=TOP,ipady=20)
        label2.place(x=n,y=m*3)
       
       
        #PLACING THE DROP DOWN
        dropDown1.place(x=n,y=m*6)
       
        #PLACING BUTTONS
        button1.place(x=n,y=m*7)
        button2.place(x=n+50,y=m*7)
       
        button3.place(x=n,y=m*9.5)
       
        button4.place(x=n+300,y=m*10)
        button5.place(x=n+380,y=m-20)

        button6.place(x=n+300,y=m*6)
        button7.place(x=n+300,y=m*7)
        button8.place(x=n+300,y=m*8)
        button9.place(x=n+300,y=m*9)



class OrdinaryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #Options for drop down just an example need to be implemented
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
        label2 = Label(self, text="Welcome to you Home Page\n\nHere are your Documents:")
        label2.config(font=("Courier", 20))
        
        #DROP DOWN
        ##REFRENE FOR DROP DOWN
        '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
        #doc1, doc 2 need to be replaced by the bakedn data
        dropDown1 = OptionMenu(self, variable, *OPTIONS)
        
        
        #BUTTONS
        button1 = tk.Button(self, text="Open",command=lambda:controller.show_frame("DocumentPage"))
                            # NEEDED TO PULL DOCUMENT FROM BACKEND)
        
        button2=tk.Button(self,text="Delete")#command=lambda:NEED A FUNCTION TO DELETE A SELECTED DOCUMENT FROM BACKEND
       
        button3=tk.Button(self, fg="red",text="Create A\nNew Document ",command=lambda:controller.show_frame("DocumentPage"))

        button4=tk.Button(self,text="Request Update")#command=lambda:NEED TO SEND REQUEST TO SUPER USER FOR UPDATING
        button5=tk.Button(self, text="Manage Invitations")#command=lambda:NEED TO CHECK FROM BACKEND IF ANYONE INVITED
        button6=tk.Button(self, text="Log Out",fg="blue",command=lambda:controller.show_frame("MainPage"))
        
        #PLACING THE LABELS
        n = 150
        m = 50
        label_type.pack(side=BOTTOM)
        label1.pack(side=TOP,ipady=20)
        label2.place(x=n,y=m*3)
        
        
        #PLACING THE DROP DOWN
        dropDown1.place(x=n,y=m*6)

        #PLACING BUTTONS
        button1.place(x=n,y=m*7)
        button2.place(x=n+50,y=m*7)
        
        button3.place(x=n,y=m*9.5)
        button4.place(x=n+300,y=m*9.5)
        button5.place(x=n+300,y=m*10)
        button6.place(x=n+380,y=m-20)

class GuestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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
        label2 = Label(self, text="Welcome to the Home Page, Guest\nHere are the Documents\nSelect a document you want to view:")
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



def main():
    #print("Phonebook App\n")
    app = Application()
    app.mainloop()

#print("\n- End of Phonebook\n")

if __name__ == "__main__":
    main()


