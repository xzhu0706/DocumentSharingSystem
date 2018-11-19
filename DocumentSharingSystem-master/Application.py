import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
from MainPage import *
from SignupPage import *
from SuperPage import *
from OrdinaryPage import *
from GuestPage import *
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
        data =[MainPage,SignupPage,OrdinaryPage,GuestPage,SuperPage,DocumentPage]
        
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



def main():
    #print("Phonebook App\n")
    app = Application()
    app.mainloop()

#print("\n- End of Phonebook\n")

if __name__ == "__main__":
    main()


