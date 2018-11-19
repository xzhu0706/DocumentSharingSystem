import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
from MainPage import *
from SignupPage import *
from SuperUser import *
from OrdinaryUser import *
from Guest import *
from DocumentPage import *


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
        data =[MainPage,SignupPage,OrdinaryUser,Guest,SuperUser,DocumentPage]
        
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
        
    def check_user(self, name, password):
        user_info_file = open("user_info", "r") #"r": read only
        #the while loop reads users' info and matches usernames and passwords
        while True:
            user_id_string = user_info_file.readline()
            if user_id_string == '':
                break
            user_id = int(user_id_string)
            user_name = user_info_file.readline() #read user_name
            user_name = user_name.replace("\n", "")
            user_password = user_info_file.readline() #read user_password
            user_password = user_password.replace("\n", "")
            user_type = user_info_file.readline() #read user_type
            user_type = user_type.replace("\n", "")
            user_info_file.readline() #skip *
            
            if (name == user_name and password == user_password):
                frame = self.page_array[user_type]
                frame.tkraise()


def main():
    #print("Phonebook App\n")
    app = Application()
    app.mainloop()

#print("\n- End of Phonebook\n")

if __name__ == "__main__":
    main()


