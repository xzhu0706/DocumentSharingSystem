import tkinter as tk
from tkinter import ttk
import DocumentsManager
import AccountsManager
import DocumentViewerPage
import pandas as pd
class Guest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.selected_docid = ''

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings


        self.docs_section = ttk.Treeview(self, height=6, show=['headings'],
                                    columns=['id', 'title', 'owner', 'scope', 'views', 'time'],
                                    style="mystyle.Treeview")
        self.docs_section.heading('id', text="id", anchor=tk.CENTER)
        self.docs_section.heading('title', text='Title', anchor=tk.CENTER)
        self.docs_section.heading('owner', text='Owner', anchor=tk.CENTER)
        self.docs_section.heading('scope', text='Scope', anchor=tk.CENTER)
        self.docs_section.heading('views', text='Views', anchor=tk.CENTER)
        self.docs_section.heading('time', text='Last Modified at', anchor=tk.CENTER)
        self.docs_section.column('id', minwidth=0, width=30, stretch=tk.NO)
        self.docs_section.column('title', minwidth=0, width=140, stretch=tk.NO)
        self.docs_section.column('owner', minwidth=0, width=100, stretch=tk.NO)
        self.docs_section.column('scope', minwidth=0, width=100, stretch=tk.NO)
        self.docs_section.column('views', minwidth=0, width=50, stretch=tk.NO)
        self.docs_section.column('time', minwidth=0, width=150, stretch=tk.NO)
        self.docs_section.bind('<Button-1>', self.on_select_doc)

        scroll_bar = ttk.Scrollbar(self,orient='vertical', command=self.docs_section.yview)
        self.docs_section.configure(yscroll=scroll_bar.set)


        label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
        label1 = tk.Label(self, text="ShareWithME")
        label1.config(font=("Courier", 35, 'bold'))
        label2 = tk.Label(self, text="Welcome to your Home Page, {}!\nSelect a document:".format(controller.get_username()))
        label2.config(font=("Courier", 20))

        #BUTTONS
        open_doc_button = tk.Button(self, text="Open", command=self.open_doc)
        ## TODO: NEED TO CHANGE

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        suggest_taboo_button = tk.Button(self, text="Suggest Taboo Words", command=lambda:self.taboo_words_suggested())

        #PLACING THE LABELS
        n = 150
        m = 50
        label_type.pack(side=tk.BOTTOM)
        label1.pack(side=tk.TOP,ipady=20)
        label2.place(x=n-50,y=m*3)

        #PLACING THE DOCUMENT TREEVIEW
        self.docs_section.place(x=n-125,y=m*5+30)
        scroll_bar.pack(side=tk.RIGHT)
        scroll_bar.place(x=580,y=m*5+60)


        #PLACING BUTTONS
        open_doc_button.place(x=n-50,y=m*8+10)
        back_button.place(x=n+100, y=m*8+10)
        suggest_taboo_button.place(x=n+300, y=m*10.5)


    def on_select_doc(self, event):
        self.selected_docid = int(self.docs_section.identify_row(event.y))

    def open_doc(self):
        if self.selected_docid:
            if self.controller.get_usertype() == 'Guest':
                self.controller.opened_docid = self.selected_docid
                self.controller.create_doc_viewer_page()
                self.controller.show_frame('DocumentViewerPage')
                DocumentsManager.inc_views_count(self.selected_docid)
            else:
                # TODO: need to check if OU/SU is contributor or owner
                print('TODO')
        else:
            tk.messagebox.showerror("", "Please select a document!")

    def fetch_docs(self):
        if self.controller.get_usertype() == 'Guest':
            docs = DocumentsManager.get_docs_for_gu()
            print('is a guest')
        else:
            # TODO: fetch docs for OU and SU
            #docs = DocumentsManager.get_own_docs(self.controller.get_userid())
            docs = pd.read_csv("database/Documents.csv", index_col=0)
        print('fetching')
        print(self.controller.get_usertype())
        docs_tuple_list = []
        for docid, row in docs.iterrows():
            docs_tuple_list.append(
                (docid,
                 row['title'],
                 AccountsManager.get_username(row['owner_id']),
                 row['scope'],
                 row['views_count'],
                 row['modified_at']
                 ))
        for doc in self.docs_section.get_children():
            self.docs_section.delete(doc)
        for doc in docs_tuple_list:
            self.docs_section.insert('', tk.END, iid=doc[0], values=doc)


    def taboo_words_suggested(self):
        box = self.taboo_box()  # create the dialog box to ask for title and scope for creating doc
        self.wait_window(box)

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
            tk.messagebox.showinfo("", "Thanks for your suggestion!")
            print("Information updated in the database")
            self.destroy()




    #def open_doc(self, ):
