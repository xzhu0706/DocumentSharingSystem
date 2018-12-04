import tkinter as tk
import DocumentsManager
import DocumentViewerPage
import pandas as pd
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

        variable = tk.StringVar(self)
        variable.set("PLEASE SELECT A DOCUMENT")
                   ##LABELS
        label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
        label1 = tk.Label(self, text="ShareWithME")
        label1.config(font=("Courier", 35, 'bold'))
        label2 = tk.Label(self, text="Welcome to your Home Page, {}!\nSelect a document:".format(controller.get_username()))
        label2.config(font=("Courier", 20))

        #DROP DOWN
        ##REFRENE FOR DROP DOWN
        '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
        #doc1, doc 2 need to be replaced by the bakend data
        dropDown1 = tk.OptionMenu(self, variable, *OPTIONS)


        #BUTTONS
        open_doc_button = tk.Button(self,text="Open",command=lambda:controller.show_frame("DocumentViewerPage")) ## NEED TO CHANGE
        # NEEDED TO PULL THE SELECTED DOCUMENT FROM BACKEND)

        back_button = tk.Button(self,text="Back",command=lambda:controller.show_frame("MainPage"))

        suggest_taboo_button = tk.Button(self,text="Suggest Taboo Words", command=lambda:self.taboo_words_suggested())



        #PLACING THE LABELS
        n = 150
        m = 50
        label_type.pack(side=tk.BOTTOM)
        label1.pack(side=tk.TOP,ipady=20)
        label2.place(x=n-50,y=m*3)


        #PLACING THE DROP DOWN
        dropDown1.place(x=n-50,y=m*6)

        #PLACING BUTTONS
        open_doc_button.place(x=n-50,y=m*7)
        back_button.place(x=n+50, y=m*7)
        suggest_taboo_button.place(x=n+300, y=m*10.5)
    def taboo_words_suggested(self):
        box = self.taboo_box()  # create the dialog box to ask for title and scope for creating doc
        self.wait_window(box)
        print("Information updated in the database")
    class taboo_box(tk.Toplevel):
        def __init__(self):
            tk.Toplevel.__init__(self)
            self.title("Suggest Taboo Words")
            title_label = tk.Label(self, text="Suggest Taboo words seperated by space: ")
            taboo_entry = tk.Entry(self)
            submit_button = tk.Button(self, fg="red", text="Submit", command=lambda : self.on_submit(taboo_entry.get()))
            cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
            title_label.grid(row=0)
            taboo_entry.grid(row=1)
            submit_button.grid(row=2)
            cancel_button.grid(row=3)
        def on_submit(self, taboo_words):
            taboo_db = pd.read_csv("database/TabooWords.csv", index_col=0)
            taboo_list=taboo_words.split()
            new_word_id = len(taboo_db) + 1
            for i in taboo_list:
                data=[[new_word_id,i,False]]
                df = pd.DataFrame(data,columns=["word_id","word","approved"])
                with open('database/TabooWords.csv', 'a') as taboo_db:
                    df.to_csv(taboo_db, index=False, header=False)
                new_word_id=new_word_id+1
            self.destroy()




    #def open_doc(self, ):
