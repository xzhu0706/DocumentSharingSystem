import tkinter as tk
import pandas as pd
#from PIL import ImageTk, Image
import DocumentsManager

class DocumentViewerPage(tk.Frame):


    def __init__(self, parent, controller):

        self.username = controller.get_username()
        self.docid = controller.opened_docid

        self.doc_info = DocumentsManager.get_doc_info(self.docid)
        self.doc_versions = DocumentsManager.get_doc_old_versions(self.docid)
        ## TODO: display doc info and doc versions into the GUI

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label_type = tk.Label(self, text="® FourofUS 2018", fg="gray", font=controller.footer_font)
        label1 = tk.Label(self, text="ShareWithME")
        label1.config(font=("Courier", 35, 'bold'))
        label_title = tk.Label(self, text="Title")
        label_content = tk.Label(self, text="Content")
        self.title = tk.Text(self, height=1, width=30, highlightbackground="black", highlightcolor="black",
                          highlightthickness=1,
                          font=("Times New Roman", 18))
        self.title.insert(tk.INSERT,self.getTitle())
        #self.title=tk.Label(self,text=self.getTitle())
        self.content = tk.Text(self, height=25, width=60, highlightbackground="black", highlightcolor="black",
                            highlightthickness=1, )
        # need to save everythin in it lets after 10 sec
        # content.insert(CURRENT,"HellO")

        OPTIONS = [
            "Version 3",
            "Version 2",
            "Version 1"
        ]  # etc
        variable = tk.StringVar(self)
        variable.set("Old versions")

        # DROP DOWN
        ##REFRENE FOR DROP DOWN
        '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
        # need to be replaced by the bakend data
        versions_drop_down = tk.OptionMenu(self, variable, *OPTIONS)

        complain_button = tk.Button(self, text="Complain")  # ,command=lambda:)
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_warning() if controller.is_warned else controller.show_frame(
            controller.get_usertype()))  # jump back to user page

        n = 150
        m = 50

        label_type.pack(side=tk.BOTTOM)
        label1.pack(side=tk.TOP, ipady=20)
        label_title.place(x=n - 120, y=m + 10)
        self.title.place(x=n - 120, y=m + 30)
        label_content.place(x=n - 120, y=m + 70)
        self.content.place(x=n - 120, y=m + 90)
        versions_drop_down.place(x=n + 325, y=m + 20)

        complain_button.place(x=n + 325, y=m * 7)
        back_button.place(x=n + 325, y=m * 8)
    def getTitle(self):
        document_db = pd.read_csv("database/Documents.csv", delimiter=',')
        # gettig the opened document id
        doc_id = self.controller.opened_docid
        # making a list of all the documents ID in the Documents.csv
        # so that we can find the index of the opened docuemnt
        doc_id_list=list(document_db._getitem_column('doc_id'))
        # making a list of all the contents of the Docuements.csv
        doc_content_list=list(document_db._getitem_column('title'))
        # finding in which index our opened document is
        index_of_doc_id=doc_id_list.index(doc_id)
        # getting content of the opened document
        return doc_content_list[index_of_doc_id]
