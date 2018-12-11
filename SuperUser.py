import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from OrdinaryUser import *

class SuperUser(OrdinaryUser):

    def __init__(self, parent, controller):

        super(SuperUser, self).__init__(parent, controller)

        update_membership_button = tk.Button(self, text="Manage Membership")  # ,command=lambda:TO BE IMPLEMENTED BY BACKEND, can update or remove user
        taboo_words_button = tk.Button(self, text="Taboo Words", command=lambda:self.taboo_words_button())

        # PLACING THE LABELS
        n = 150
        m = 50

        update_membership_button.place(x=n + 300, y=m * 8.5)
        taboo_words_button.place(x=n + 300, y=m * 9)

    def taboo_words_button(self):
        user_box=self.display_update_taboo_box()

    class display_update_taboo_box(tk.Toplevel):

        def __init__(self):
            # this is passed as keyword in the text field of the search bar
            tk.Toplevel.__init__(self)
            self.title("Manage Taboo Words")
            taboo_db=pd.read_csv("database/TabooWords.csv")

            taboo_list=tk.Listbox(self,height=10)#,width=10
            taboo_list_approved=tk.Listbox(self,height=10)
            taboo_to_be_approve=tk.Label(self,text="To Be Approved")
            taboo_approved=tk.Label(self,text="Already Approved")


            unapproved_taboo_words=taboo_db['word'].loc[taboo_db['approved']== False].tolist()
            approved_taboo_words=taboo_db['word'].loc[taboo_db['approved']== True].tolist()

            for words in unapproved_taboo_words:
                taboo_list.insert(tk.END,words)
            for words in approved_taboo_words:
                taboo_list_approved.insert(tk.END,words)

            taboo_button_approve=tk.Button(self,text="Approve",command=lambda: self.approve_word(taboo_list,taboo_list_approved))#.get(tk.ACTIVE)))
            taboo_button_deny=tk.Button(self,text="Deny",command=lambda: self.deny_word(taboo_list,taboo_list_approved))#.get(tk.ACTIVE)))
            button_delete=tk.Button(self,text="Delete", command = lambda: self.delete_word(taboo_list_approved))

            button_cancel=tk.Button(self,text="Cancel",command=self.destroy)
            # placing the buttons:

            taboo_to_be_approve.grid(row=0,column=0)
            taboo_approved.grid(row=0,column=2)
            taboo_list.grid(row=1,column=0)
            taboo_list_approved.grid(row=1,column=2)
            taboo_button_approve.grid(row=2,column=0)
            taboo_button_deny.grid(row=2,column=1)
            button_delete.grid(row=2,column=2)
            button_cancel.grid(row=3,column=1)



        def approve_word(self,listbox,approvedlistbox):
            '''function that approes the words'''
            word=listbox.get(tk.ACTIVE)
            taboo_db=pd.read_csv("database/TabooWords.csv",index_col=0)
            taboo_db.loc[word,'approved']=True
            taboo_db.to_csv("database/TabooWords.csv")

            selection = listbox.curselection()
            listbox.delete(selection[0])
            approvedlistbox.insert(tk.END,word)
            print("{} approved as a taboo word".format(word))

        def deny_word(self,listbox,approvedlistbox):
            '''funtion that denies the word'''
            word=listbox.get(tk.ACTIVE)
            taboo_data=pd.read_csv("database/TabooWords.csv",index_col=0)
            taboo_data.drop(word,inplace=True)
            taboo_data.to_csv("database/TabooWords.csv")

            selection = listbox.curselection()
            listbox.delete(selection[0])
            print("{} denied as a taboo word".format(word))
        def delete_word(self,approvedlistbox):
            '''function that delets the already approved words'''
            word=approvedlistbox.get(tk.ACTIVE)
            taboo_data=pd.read_csv("database/TabooWords.csv",index_col=0)
            taboo_data.drop(word,inplace=True)
            taboo_data.to_csv("database/TabooWords.csv")

            selection = approvedlistbox.curselection()
            approvedlistbox.delete(selection[0])
            print("deleted {} from database".format(word))



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
