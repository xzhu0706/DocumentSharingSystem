from Guest import *
import tkinter as tk
import DocumentsManager

class OrdinaryUser(Guest):

    def __init__(self, parent, controller):

        super(OrdinaryUser, self).__init__(parent, controller)

        self.username = controller.get_username()
        self.userid = controller.get_userid()

        delete_button = tk.Button(self,
                            text="Delete")  # command=lambda:
        # TODO:NEED A FUNCTION TO DELETE A SELECTED DOCUMENT FROM BACKEND

        create_doc_button = tk.Button(self, text="Create A \n New Document ",fg="red",
                            command=lambda: self.create_new_doc())
        # create_doc_button.config(height=10, width=10);
        process_complaints_button = tk.Button(self,
                            text="Process Complaints")  # command=lambda:
        # TODO:NEED TO SHOW THE COMPLAINTS THE USER RECEIVED
        manage_invite_button = tk.Button(self,
                            text="Manage Invitations")  # command=lambda:NEED TO CHECK FROM BACKEND IF ANYONE INVITED
        logout_button = tk.Button(self, text="Log Out", fg="blue", command=lambda: controller.show_frame("MainPage"))

        search_field = tk.Entry(self)


        user_search_button = tk.Button(self, text="Search User", command=lambda: self.search_user(search_field.get()))
        document_search_button = tk.Button(self, text="Search Document", command=lambda: self.search_document(search_field.get()))

        # PLACING THE LABELS
        n = 150
        m = 50

        delete_button.place(x=n + 50, y=m * 7)
        create_doc_button.place(x=n, y=m * 9.5)
        process_complaints_button.place(x=n + 300, y=m * 9.5)
        manage_invite_button.place(x=n + 300, y=m * 10)
        logout_button.place(x=n + 380, y=m - 20)


        search_field.place(x=n-50, y=m*4.75)

        user_search_button.place(x=n+140, y=m*4.5)
        document_search_button.place(x=n+140, y=m*5)


    def create_new_doc(self):
        box = self.dialog_box()  # create the dialog box to ask for title and scope for creating doc
        self.wait_window(box)  # wait until dialog is closed (info is submitted)
        title = box.init_info['title']
        scope = box.init_info['scope']
        new_doc_id = DocumentsManager.create_new_doc(self.userid, scope, title) # get new_doc_id
        self.controller.opened_docid = new_doc_id  # set currently opened doc_id
        self.controller.create_doc_owner_page()    # create new doc_owner_page
        self.controller.show_frame("DocumentOwnerPage")  # display page
    def search_user(self,result):
        user_box=self.display_user_box(result)

    def search_document(self,result):
        user_box=self.display_document_box(result)


    class dialog_box(tk.Toplevel):

        def __init__(self):
            tk.Toplevel.__init__(self)

            self.init_info = {
                'title': '',
                'scope': ''
            }

            self.title("Creating a new document")
            title_label = tk.Label(self, text="Title: ")
            scope_label = tk.Label(self, text="Scope: ")
            title_entry = tk.Entry(self)
            OPTIONS = [
                "Private",
                "Shared",
                "Restricted",
                "Public"
            ]
            variable = tk.StringVar(self)
            variable.set("Scopes")
            scopes_drop_down = tk.OptionMenu(self, variable, *OPTIONS)
            submit_button = tk.Button(self, fg="red", text="Submit", command=lambda : self.on_submit(
                title_entry.get(), variable.get()))
            cancel_button = tk.Button(self, text="Cancel", command=self.destroy)

            title_label.grid(row=0)
            scope_label.grid(row=1)
            title_entry.grid(row=0, column=1)
            scopes_drop_down.grid(row=1, column=1)
            submit_button.grid(row=2, column=1)
            cancel_button.grid(row=2, column=0)

        def on_submit(self, title, scope):
            self.init_info['title'] = title
            self.init_info['scope'] = scope
            self.destroy()
    # this class helps is invoked to display search results of user in a document page
    class display_user_box(tk.Toplevel):

        def __init__(self,user_result):
            # this is passed as keyword in the text field of the search bar
            tk.Toplevel.__init__(self)
            self.user_result=user_result
            self.title("User Search Results")

            #reading the file for userinfo database
            user_db=pd.read_csv("database/UserInfos.csv")

            # list that stores all the user names
            user_list=list(user_db['username'])
            # list that stores all the tehcnical interest for all user in the respective index of the user
            technical_list=list(user_db['technical_interest'])
            #empty list to store the index of usernames matched
            index_list=[]
            # check if any usernames matches the searched input

            # make a list box
            username_list=tk.Listbox(self,height=10)#,width=10)
            # setting the title for the listbox
            username_list.insert(tk.END,"Users")
            # lopping through the names of usernames
            for names in user_list:
                # check if text in search bar has anything from the name in the database
                if self.user_result in names:
                    username_list.insert(tk.END,names)
                    # kepping track of the indexes added to add the corresponding technical interests
                    index_list.append(user_list.index(names))

            # make a list box for technical interest
            technicalinterest_list=tk.Listbox(self,height=10)
            # setting the title for the listbox
            technicalinterest_list.insert(tk.END,"Technical Interest")
            # looping through the indexes added in the username_list
            for index in index_list:
                # add that specific index of the technical_list
                technicalinterest_list.insert(tk.END,technical_list[index])

            # cancel button to go back to the main page
            cancel_button=tk.Button(self,text="Cancel",command=self.destroy)#,command=lambda:mylistbox.get(ACTIVE))

            # setting up the layout of the dialog box
            username_list.grid(row=0,column=0)
            technicalinterest_list.grid(row=0,column=1)
            cancel_button.grid(row=1,column=0)

            # this is the case when there is no match which simply destroys the box
            # then prints an error messagebox in the screen
            # as index_list is updated when a match is found its length being 0 confrims no match
            if(len(index_list)==0):
                self.destroy()
                tk.messagebox.showerror("Error","No Such User found")

    # thie class pops the dialogue box for the documents
    class display_document_box(tk.Toplevel):

        def __init__(self,document_result):
            tk.Toplevel.__init__(self)
            # this is passed as keyword in the text field of the search bar
            self.document_result=document_result
            self.title("Document Search Results")

            #reading the file for Document database
            document_db=pd.read_csv("database/Documents.csv")

            # list that stores all the user names
            document_list=list(document_db['title'])


            # make a list box
            document_listbox=tk.Listbox(self,height=10)
            # lopping through the document's title
            counter=0
            for documents in document_list:
                # check the document that match keywords entered in the search bar
                if self.document_result in documents:
                    document_listbox.insert(tk.END,documents)
                    counter=counter+1

            # cancel button to go back to the main page
            cancel_button=tk.Button(self,text="Cancel",command=self.destroy)
            # open button to open th document
            open_button=tk.Button(self,text="Open")#,command=self.destroy)#,command=lambda:mylistbox.get(ACTIVE))


            # setting up the layout of the dialog box
            document_listbox.grid(row=0,column=0)
            cancel_button.grid(row=1,column=0)
            open_button.grid(row=1,column=1)

            # this is the case when there is no match which simply destroys the box
            # then prints an error messagebox in the screen
            # as counter is updated when a match is found it being 0 confrims no match
            if(counter==0):
                self.destroy()
                tk.messagebox.showerror("Error","No Such Document found")










# class OrdinaryUser(tk.Frame):
#
#     def __init__(self, parent, controller, userid, username):
#
#         self.username = username
#         self.userid = userid
#
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         # self.user_info = controller.get_user()
#         # print(self.user_info)
#         # print(controller.username)
#
#         #Options for drop down just an example need to be implemented
#         OPTIONS = [
#                    "DOCUMENT 1",
#                    "DOCUMENT 2",
#                    "DOCUMENT 3"
#                    ] #etc
#         variable = StringVar(self)
#         variable.set("PLEASE SELECT A DOCUMENT")
#         ##LABELS
#         label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
#         label1 = tk.Label(self, text="ShareWithME")
#         label1.config(font=("Courier", 35, 'bold'))
#         label2 = Label(self, text="Welcome to your Home Page, {}!\n\nHere are your Documents:".format(self.username))
#         label2.config(font=("Courier", 20))
#
#         #DROP DOWN
#         ##REFRENcE FOR DROP DOWN
#         '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
#         #doc1, doc 2 need to be replaced by the bakedn data
#         dropDown1 = OptionMenu(self, variable, *OPTIONS)
#
#
#         #BUTTONS
#         button1 = tk.Button(self, text="Open",command=lambda:controller.show_frame("DocumentPage"))
#                             # NEEDED TO PULL DOCUMENT FROM BACKEND)
#
#         button2=tk.Button(self,text="Delete")#command=lambda:NEED A FUNCTION TO DELETE A SELECTED DOCUMENT FROM BACKEND
#
#         button3=tk.Button(self, fg="red",text="Create A\nNew Document ",command=lambda:controller.show_frame("DocumentPage"))
#         ### NEED TO CHANGE!!!
#
#         button4=tk.Button(self,text="Request Update")#command=lambda:NEED TO SEND REQUEST TO SUPER USER FOR UPDATING
#         button5=tk.Button(self, text="Manage Invitations")#command=lambda:NEED TO CHECK FROM BACKEND IF ANYONE INVITED
#         button6=tk.Button(self, text="Log Out",fg="blue",command=lambda:controller.show_frame("MainPage"))
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
#         button4.place(x=n+300,y=m*9.5)
#         button5.place(x=n+300,y=m*10)
#         button6.place(x=n+380,y=m-20)
