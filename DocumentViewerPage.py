import tkinter as tk
import pandas as pd
#from PIL import ImageTk, Image
import DocumentsManager

class DocumentViewerPage(tk.Frame):


    def __init__(self, parent, controller):

        self.username = controller.get_username()
        self.userid = controller.get_userid()
        self.docid = controller.opened_docid

        self.doc_info = DocumentsManager.get_doc_info(self.docid)
        self.doc_versions = DocumentsManager.get_doc_old_versions(self.docid)

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

        #### display doc info here ####
        self.title.insert(tk.INSERT, self.filter_taboo_words(self.doc_info['title'], ' '))
        if self.doc_info['current_seq_id'] != '-':
            self.content.insert(tk.INSERT, self.filter_taboo_words(self.doc_info['content'], '\n'))
        ## TODO: display lock status (and locker)
        ## TODO: display last modified date and last modifier
        ## TODO: display owner


    def filter_taboo_words(self, content, separator):
        '''separator is blank space if content is doc title
            separator is newline if content is doc content
            This function returns a filtered content without appearance of taboo words'''
        words_used = content.split(separator)
        taboo_words = self.get_taboo_words()
        filtered_content = []
        for word in words_used:
            if word in taboo_words:
                filtered_content.append('UNK')
            else:
                filtered_content.append(word)
        if separator == ' ':
            return ' '.join(filtered_content)
        else:
            return '\n'.join(filtered_content)

    def get_taboo_words(self):
        taboo_db = pd.read_csv("database/TabooWords.csv")
        taboo_list = taboo_db.loc[taboo_db['approved'] == True]['word'].tolist()
        return taboo_list
