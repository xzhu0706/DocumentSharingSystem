from DocumentEditorPage import *
import DocumentsManager
import AccountsManager
import InvitationsManager

class DocumentOwnerPage(DocumentEditorPage):

    def __init__(self, parent, controller):

        super(DocumentOwnerPage, self).__init__(parent, controller)

        OPTIONS = [
            "Private",
            "Shared",
            "Restricted",
            "Public"
        ]
        self.selected_scope_var = tk.StringVar(self)
        self.selected_scope_var.set(self.doc_info['scope'])

        scopes_drop_down = tk.OptionMenu(self, self.selected_scope_var, *OPTIONS)

        manage_contributor_button = tk.Button(self, text="Manage Contributors", command=self.manage_contributors)
        set_scope_button = tk.Button(self, fg="red", text=" Set ", command=self.set_scope)

        n = 150
        m = 50

        manage_contributor_button.place(x=n+325, y=m*6)
        set_scope_button.place(x=n+420, y=m+51)
        scopes_drop_down.place(x=n+325, y=m+50)

    def manage_contributors(self):
        if self.doc_info['scope'] != 'Shared':
            tk.messagebox.showerror("", "You can only manage contributors if the document is Shared. Please"
                                        "change the scope of document to Shared if you want to do so.")
        else:
            self.ManageContributorsBox(self.docid)

    def set_scope(self):
        current_scope = self.doc_info['scope']
        new_scope = self.selected_scope_var.get()
        if current_scope == 'Shared':
            msg_box = tk.messagebox.askquestion("Change Scope",
                                                "This is a Shared document. Are you sure you want to change the scope to {}? "
                                                "If you do, all contributors of this document will be removed.".format(new_scope),
                                                icon="warning")
            if msg_box == 'yes':
                DocumentsManager.set_scope(self.docid, new_scope)
                DocumentsManager.remove_all_contributor(self.docid)
                tk.messagebox.showinfo("", "Set scope successfully!")
                self.fetch_status()
            return
        DocumentsManager.set_scope(self.docid, new_scope)
        tk.messagebox.showinfo("", "Set scope successfully!")
        self.fetch_status()

    class ManageContributorsBox(tk.Toplevel):
        # This class is a pop up box that let user to manage contributors

        def __init__(self, docid): # pass in docid to constructor
            tk.Toplevel.__init__(self)

            self.contributors = DocumentsManager.get_contributors(docid)
            self.docid = docid

            self.title("Manage Contributors")
            contributors_label = tk.Label(self, text="Contributors")
            all_users_label = tk.Label(self, text="All Users")

            #################################################################
            # drop down for all users
            self.all_users_dict = AccountsManager.get_all_users_id_name()
            self.all_users_name_list = [self.all_users_dict[user] for user in self.all_users_dict]
            self.selected_user_var = tk.StringVar(self)
            self.selected_user_var.set("All Users")
            all_users_drop_down = tk.OptionMenu(self, self.selected_user_var, *self.all_users_name_list)

            #################################################################
            # list box for contributors
            # remember index for each contributor in the list
            self.contributor_id_list_in_index_order = []
            self.contributors_list_box = tk.Listbox(self, height=6)
            for contributor_id in self.contributors:
                self.contributors_list_box.insert(tk.END, AccountsManager.get_username(contributor_id))
                self.contributor_id_list_in_index_order.append(contributor_id)

            #################################################################

            add_button = tk.Button(self, fg="red", text="Add", command=self.add_contributor)
            remove_button = tk.Button(self, fg="red", text="Remove", command=self.remove_contributor)
            back_button = tk.Button(self, text="Back", command=self.destroy)


            contributors_label.grid(row=0)
            all_users_label.grid(row=1)

            self.contributors_list_box.grid(row=0, column=1)
            all_users_drop_down.grid(row=1, column=1)

            add_button.grid(row=1, column=2)
            remove_button.grid(row=0, column=2)
            back_button.grid(row=2, column=2)

        def add_contributor(self):
            selected_user_name = self.selected_user_var.get()
            selected_user_id = ''

            for id, name in self.all_users_dict.items():
                if name == selected_user_name:
                    selected_user_id = id

            if selected_user_id in self.contributor_id_list_in_index_order:
                tk.messagebox.showerror("", "The user is already a contributor!")
            elif DocumentsManager.is_owner(selected_user_id, self.docid):
                tk.messagebox.showerror("", "You cannot add yourself to be the contributor!")
            elif InvitationsManager.is_rejected(selected_user_id, self.docid):
                tk.messagebox.showerror("", "{} has rejected your invitation!".format(selected_user_name))
            elif InvitationsManager.is_invited(selected_user_id, self.docid):
                tk.messagebox.showerror("", "You have already sent the invitation before!"
                                            "Please wait for {} to accept it.".format(selected_user_name))
            else:
                InvitationsManager.send_invitation(selected_user_id, self.docid)
                tk.messagebox.showinfo("", "Invitation has been sent to {}!".format(selected_user_name))

        def remove_contributor(self):
            selected_index = self.contributors_list_box.curselection()[0]
            selected_userid = self.contributor_id_list_in_index_order[selected_index]
            DocumentsManager.remove_contributor(selected_userid, self.docid)
            self.contributors_list_box.delete(selected_index)
            self.contributor_id_list_in_index_order.pop(selected_index)
