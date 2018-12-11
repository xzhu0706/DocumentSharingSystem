import tkinter as tk
from tkinter import ttk
import DocumentsManager
import AccountsManager
import InvitationsManager
import pandas as pd

class Guest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = controller.get_username()
        self.userid = controller.get_userid()

        self.selected_docid = ''

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings


        self.docs_section = ttk.Treeview(self, height=6, show=['headings'],
                                    columns=['title', 'owner', 'scope', 'views', 'time'],
                                    style="mystyle.Treeview")
        self.docs_section.heading('title', text='Title', anchor=tk.CENTER)
        self.docs_section.heading('owner', text='Owner', anchor=tk.CENTER)
        self.docs_section.heading('scope', text='Scope', anchor=tk.CENTER)
        self.docs_section.heading('views', text='Views', anchor=tk.CENTER)
        self.docs_section.heading('time', text='Last Modified at', anchor=tk.CENTER)
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
        refresh_button = tk.Button(self, text="Refresh", command=self.fetch_docs_for_home_page)

        back_button = tk.Button(self, text="Back",
                                command=self.destroy)
        suggest_taboo_button = tk.Button(self, text="Suggest Taboo Words", command=lambda: self.taboo_words_suggested())

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
        refresh_button.place(x=n+390, y=m*5+5)

        ## Call fetch docs function
        self.fetch_docs_for_home_page()


    def on_select_doc(self, event):
        selected_doc = (self.docs_section.identify_row(event.y))
        if selected_doc:
            self.selected_docid = int(selected_doc)

    def open_doc(self):
        if self.selected_docid:
            self.controller.opened_docid = self.selected_docid
            DocumentsManager.inc_views_count(self.selected_docid)
            if self.controller.get_usertype() == 'Guest':
                self.controller.create_doc_viewer_page()
            else:
                if DocumentsManager.is_owner(self.userid, self.selected_docid):
                    self.controller.create_doc_owner_page()
                elif DocumentsManager.is_contributor(self.userid, self.selected_docid, self.controller.is_su()):
                    self.controller.create_doc_editor_page()
                elif DocumentsManager.is_viewer(self.selected_docid):
                    self.controller.create_doc_viewer_page()
                else:
                    tk.messagebox.showerror("", "Sorry, you don't have access to this document!")
        else:
            tk.messagebox.showerror("", "Please select a document!")

    def fetch_docs_for_home_page(self):
        if self.controller.get_usertype() == 'Guest':
            docs = DocumentsManager.get_docs_for_gu()
        else:
            docs = DocumentsManager.get_docs_for_ou(self.userid)
        self.refresh_doc_section(docs)

    def refresh_doc_section(self, docs):
        '''Input docs should be a dataframe, this function refresh content in docs_section treeview'''
        for old_doc in self.docs_section.get_children():
            self.docs_section.delete(old_doc)
        if not docs.empty:
            for docid, row in docs.iterrows():
                doc_info_tuple = (row['title'],
                                  AccountsManager.get_username(row['owner_id']),
                                  row['scope'],
                                  int(row['views_count']),  # make sure it's integer (sometimes it becomes float idk why)
                                  row['modified_at'])
                self.docs_section.insert('', tk.END, iid=docid, values=doc_info_tuple)

    def taboo_words_suggested(self):
        self.TabooBox()

    class TabooBox(tk.Toplevel):

        def __init__(self):
            tk.Toplevel.__init__(self)
            self.title("Suggest Taboo Words")
            title_label = tk.Label(self, text="Suggest taboo words separated by space: ")
            taboo_entry = tk.Entry(self)
            submit_button = tk.Button(self, fg="red", text="Submit", command=lambda : self.on_submit(taboo_entry.get()))
            cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
            title_label.grid(row=0)
            taboo_entry.grid(row=1)
            submit_button.grid(row=2)
            cancel_button.grid(row=3)

        def on_submit(self, taboo_words):
            taboo_list=taboo_words.split()

            for i in taboo_list:
                data=[[i,False]]
                df = pd.DataFrame(data,columns=["word","approved"])
                with open('database/TabooWords.csv', 'a') as taboo_db:
                    df.to_csv(taboo_db, index=False, header=False)
                new_word_id=new_word_id+1
            tk.messagebox.showinfo("", "Thanks for your suggestion!")
                
            print("Information updated in the database")
            self.destroy()

