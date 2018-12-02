############################################################################
#Name:Application.py
#Description: This program opens up a empty window and shows the MainPage
############################################################################
import tkinter as tk
from tkinter import *
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
        self.__username = 'Guest'
        self.__userid = '0'
        self.__usertype = 'Guest'
        self.__docid = ''
        
        tk.Tk.__init__(self)
        self.title(app_name)
        self.geometry(window_dimensions)
        self.resizable(0,0)
        self.title_font = font.Font(family='Courier', size=32, weight="bold", underline=True)
        self.footer_font = font.Font(family='Comic Sans MS', size=12, weight='bold',slant="italic")
        self.subheader_font = font.Font(family='Times', size=12, weight='bold',underline=True)
        # the container is where we'll stack a bunch of frames on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand= True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Classes array
        self.page_array = {}
        data = [MainPage, SignupPage, Guest]

        for page in data:
            page_name = page.__name__
            current_page = page(parent=self.container, controller=self)
            print('created {}'.format(page))

            self.page_array[page_name] = current_page

            # put all of the pages in the same location; the one on the TOP of the stacking order --> visible.
            current_page.grid(row=0, column=0, sticky="nsew")
        
        #self.show_frame("MainPage")
        self.create_doc_page()
        self.show_frame("DocumentPage")
        
    def show_frame(self, page_name):
        frame = self.page_array[page_name]
        frame.tkraise()

    def set_user(self, username, userid, usertype):
        self.__username = username
        self.__userid = userid
        self.__usertype = usertype
        print('user is logged in as: ' + username)
        # create page for user
        if usertype == 'SuperUser':
            self.create_su_page()
        elif usertype == 'OrdinaryUser':
            self.create_ou_page()

    def get_username(self):
        return self.__username

    def get_userid(self):
        return self.__userid

    def get_usertype(self):
        return self.__usertype

    def get_docid(self):
        return self.__docid

    def create_su_page(self):
        page_name = SuperUser.__name__
        su_page = SuperUser(parent=self.container, controller=self)
        self.page_array[page_name] = su_page
        su_page.grid(row=0, column=0, sticky="nsew")
        print('created {} for user id {}'.format(su_page, self.__userid))

    def create_ou_page(self):
        page_name = OrdinaryUser.__name__
        ou_page = OrdinaryUser(parent=self.container, controller=self)
        self.page_array[page_name] = ou_page
        ou_page.grid(row=0, column=0, sticky="nsew")
        print('created {} for user id {}'.format(ou_page, self.__userid))

    def create_doc_page(self):
        page_name = DocumentPage.__name__
        doc_page = DocumentPage(parent=self.container, controller=self)
        self.page_array[page_name] = doc_page
        doc_page.grid(row=0, column=0, sticky="nsew")
        print('created {} for document id {}'.format(doc_page, self.__docid))
        
#main()
def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()

