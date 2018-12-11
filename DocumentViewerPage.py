import tkinter as tk
import pandas as pd
#from PIL import ImageTk, Image
import DocumentsManager
import AccountsManager
import InvitationsManager

class DocumentViewerPage(tk.Frame):

    def __init__(self, parent, controller):

        self.username = controller.get_username()
        self.userid = controller.get_userid()
        self.docid = controller.opened_docid
        self.controller = controller

        self.doc_info = DocumentsManager.get_doc_info(self.docid)
        self.doc_versions = DocumentsManager.get_doc_old_versions(self.docid)
        self.owner_name = AccountsManager.get_username(self.doc_info['owner_id'])

        tk.Frame.__init__(self, parent)

        self.lock_status_var = tk.StringVar(self)
        self.title_var = tk.StringVar(self)
        self.content_var = tk.StringVar(self)
        self.modified_time_var = tk.StringVar(self)
        self.modified_user_var = tk.StringVar(self)
        self.last_modified_var = tk.StringVar(self)
        self.scope_var = tk.StringVar(self)
        lock_status_label = tk.Label(self, textvariable=self.lock_status_var, fg="grey")
        last_modified_label = tk.Label(self, textvariable=self.last_modified_var, fg="grey")
        scope_label = tk.Label(self, textvariable=self.scope_var, fg="grey")
        owner_label = tk.Label(self, text="Owned by {}".format(self.owner_name), fg="green")

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

        # For version history drop down
        self.version_var = tk.StringVar(self)
        self.selected_version = ''
        self.doc_versions_list = []
        self.versions_drop_down = tk.OptionMenu(self, self.version_var, None)

        # TODO: need function and GUI for complaints
        complain_button = tk.Button(self, text="Complain")  # ,command=lambda:)
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_warning() if controller.is_warned else self.destroy())

        n = 150
        m = 50

        label_type.pack(side=tk.BOTTOM)
        label1.pack(side=tk.TOP, ipady=20)
        label_title.place(x=n - 120, y=m + 10)
        self.title.place(x=n - 120, y=m + 30)
        label_content.place(x=n - 120, y=m + 70)
        self.content.place(x=n - 120, y=m + 90)
        self.versions_drop_down.place(x=n + 325, y=m + 20)

        complain_button.place(x=n + 325, y=m * 7)
        back_button.place(x=n + 325, y=m * 8)
        lock_status_label.place(x=n + 70, y=m * 10 + 20)
        last_modified_label.place(x=n + 70, y=m * 10 + 40)
        scope_label.place(x=n - 40, y=m + 70)
        owner_label.place(x=n + 160, y=m + 70)

        # display doc info
        self.refresh_content()

    def fetch_title_and_content(self):
        # delete old content and insert new content
        self.doc_info = DocumentsManager.get_doc_info(self.docid)
        if self.doc_info['current_seq_id'] != '-':
            self.title.delete(1.0, tk.END)
            self.title.insert(tk.INSERT, self.filter_taboo_words(str(self.doc_info['title']), ' '))
            self.content.delete(1.0, tk.END)
            self.content.insert(tk.INSERT, self.filter_taboo_words(str(self.doc_info['content']), '\n'))
        else:
            # do not filter the initial title upon creating new doc
            self.title.delete(1.0, tk.END)
            self.title.insert(tk.INSERT, self.doc_info['title'])

    def fetch_status(self):
        self.doc_info = DocumentsManager.get_doc_info(self.docid)
        # update lock status
        if self.doc_info['is_locked'] == False:
            self.lock_status_var.set("Document is unlocked")
        else:
            locker = DocumentsManager.get_locker(self.docid)
            self.lock_status_var.set("Document is currently locked by {}".format(locker['name']))
        # update scope
        self.scope_var.set("This is a {} document".format(self.doc_info['scope']))
        # update last modifier and time
        self.last_modified_var.set(
            "Last modified by {} at {}".format(AccountsManager.get_username(int(self.doc_info['modified_by'])),
                                               self.doc_info['modified_at'])
        )

    def fetch_old_versions(self):
        # TODO: need to try with more example, currently works with docid = 37 (with editing commands in versions db)
        self.doc_versions = DocumentsManager.get_doc_old_versions(self.docid)

        if self.doc_info['current_seq_id'] != '-':
            current_seq_id = self.doc_info['current_seq_id']
            self.doc_versions_list = ['Version {}'.format(current_seq_id.split('-')[1])]
            self.selected_version = self.doc_versions_list[0]
            self.version_var.set(self.doc_versions_list[0]) # initial selected version is current version

        if not self.doc_versions.empty:
            print(self.doc_versions)
            for seq_id, row in self.doc_versions.iterrows():
                self.doc_versions_list.append('Version {}'.format(seq_id.split('-')[1]))
            print(self.doc_versions_list)
        self.versions_drop_down['menu'].delete(0, tk.END)
        for version in self.doc_versions_list:
            self.versions_drop_down['menu'].add_command(label=version,
                                                        command=lambda value=version: self.version_selected(value))

    def refresh_content(self):
        # Can use this function to refresh content
        self.fetch_title_and_content()
        self.fetch_status()
        self.fetch_old_versions()

    def version_selected(self, value):
        # retrieve selected version:
        self.version_var.set(value)
        self.selected_version = value
        print(value)
        selected_seq_id = '{}-{}'.format(self.docid, value.split()[1])
        print(selected_seq_id)
        self.content.delete(1.0, tk.END)
        # if selected version is current version then display current content
        if selected_seq_id == self.doc_info['current_seq_id']:
            self.content.insert(tk.INSERT, self.filter_taboo_words(self.doc_info['content'], '\n'))
        else:
            old_version_content = DocumentsManager.retrieve_old_version(selected_seq_id)
            self.content.insert(tk.INSERT, self.filter_taboo_words(old_version_content, '\n'))


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
