from OrdinaryUser import *

class SuperUser(OrdinaryUser):

    def __init__(self, parent, controller):

        super(SuperUser, self).__init__(parent, controller)

        # TODO: Baivab: need to work on update membership
        update_membership_button = tk.Button(self, text="Manage Membership",command=lambda:self.manage_membership())
        taboo_words_button = tk.Button(self, text="Manage Taboo Words", command=lambda: self.manage_taboo_words())

        # PLACING THE LABELS
        n = 150
        m = 50

        update_membership_button.place(x=n + 300, y=m * 8.5)
        taboo_words_button.place(x=n + 300, y=m * 9)

    def manage_taboo_words(self):
        self.ManageTabooWordsBox()

    def manage_membership(self):
        self.ManageMembership()

    class ManageTabooWordsBox(tk.Toplevel):

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

            taboo_button_approve=tk.Button(self,text="Approve",command=lambda: self.approve_word(taboo_list,taboo_list_approved))
            taboo_button_deny=tk.Button(self,text="Deny",command=lambda: self.deny_word(taboo_list,taboo_list_approved))
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
            '''function that deletes the already approved words'''
            word=approvedlistbox.get(tk.ACTIVE)
            taboo_data=pd.read_csv("database/TabooWords.csv")
            index = taboo_data.loc[taboo_data['word'] == word].index.tolist()[0]
            taboo_data.drop(index,inplace=True)
            taboo_data.to_csv("database/TabooWords.csv", index=False)

            selection = approvedlistbox.curselection()
            approvedlistbox.delete(selection[0])
            print("deleted {} from database".format(word))
    class ManageMembership(tk.Toplevel):

        def __init__(self):
            # this is passed as keyword in the text field of the search bar
            tk.Toplevel.__init__(self)
            self.title("Manage Membership")
            pending_db=pd.read_csv("database/PendingApplications.csv")
            user_info_db=pd.read_csv("database/UserInfos.csv")
            pending_list=ttk.Treeview(self,height=8,show=['headings'],
                                                    columns=['user', 'interest'])
            pending_list.heading('user', text='User')
            pending_list.heading('interest', text='Technical Interest')
            pending_list.column('user', minwidth=0, width=100)
            pending_list.column('interest', minwidth=0, width=150)


            vsb = ttk.Scrollbar(self, orient="vertical", command=pending_list.yview)
            pending_list.configure(yscrollcommand=vsb.set)
                                        #,width=10
            user_list=tk.Listbox(self,height=9)
            pending_label=tk.Label(self,text="Pending Applications")
            user_label=tk.Label(self,text="Ordinary Users")

            pending_names=pending_db['username'].tolist()
            pending_technical_interset=pending_db['technical_interest'].tolist()
            user_names=user_info_db['username'].loc[user_info_db['usertype'] == 'OrdinaryUser'].tolist()
            tree_dict={}
            for i in range(0,len(pending_names)):
                tree_dict[pending_names[i]]=pending_technical_interset[i]

            for key in tree_dict:
                pending_list.insert('',tk.END,values=(key,tree_dict[key]))
            for name in user_names:
                user_list.insert(tk.END,name)

            button_approve=tk.Button(self,text="Approve",command=lambda: self.approve_pending(pending_list,user_list))#.get(tk.ACTIVE)))
            button_deny=tk.Button(self,text="Deny", command=lambda: self.deny_pending(pending_list))#.get(tk.ACTIVE)))
            button_delete_user=tk.Button(self,text="Remove", command = lambda: self.remove_user(user_list))

            button_cancel=tk.Button(self,text="Cancel",command=self.destroy)

            pending_label.grid(row=0,column=0)
            user_label.grid(row=0,column=2)
            pending_list.grid(row=1,column=0)
            user_list.grid(row=1,column=2)
            button_approve.grid(row=2,column=0)
            button_deny.grid(row=3,column=0)
            button_delete_user.grid(row=2,column=2)
            button_cancel.grid(row=3,column=2)

        def deny_pending(self,pendinguser_list):
            '''this fucntion takes a listbox and removes the seleted user from pending db'''
            # geting the username selected
            current_item=pendinguser_list.focus()
            username=pendinguser_list.item(current_item)['values'][0]


            # removing the user from the db
            AccountsManager.remove_pending_user(username)

            #removing the db from the listbox
            selection = pendinguser_list.selection()[0]
            pendinguser_list.delete(selection)

            # printing the final output
            print("denied {}'s account".format(username))

        def approve_pending(self,pendinguser_list,ordinary_list):
            '''this fucntion take two listbox's and adds the selected user to the user db '''
            # maintaining a list to ad in db
            userinfo={}

            # getting the selected usernaem
            current_item=pendinguser_list.focus()
            username=pendinguser_list.item(current_item)['values'][0]
            #reading the peding database to get password and tenchnical interest
            pending_db=pd.read_csv("database/PendingApplications.csv")

            # getting the password and technical interest from the databse
            password=((pending_db.loc[pending_db['username']==username]['password']).tolist())[0]
            technical_interest=((pending_db.loc[pending_db['username']==username]['technical_interest']).tolist())[0]

            #assigning each values to the dictionary
            userinfo['usertype']='OrdinaryUser'
            userinfo['username']=username
            userinfo['password']=password
            userinfo['technical_interest']=technical_interest


            # adding the user to the UserInfo databse
            AccountsManager.add_user(userinfo)
            # removing it from the pending databse
            AccountsManager.remove_pending_user(username)

            # moving the user to ordinary list from the pending list
            ordinary_list.insert(tk.END,username)

            selection = pendinguser_list.selection()[0]
            pendinguser_list.delete(selection)

            # final output
            print("Aprroved {}'s account.".format(username))


        def remove_user(self,ordinary_list):
            username=ordinary_list.get(tk.ACTIVE)
            userinfo=AccountsManager.get_all_users_id_name()
            user_id=(list(userinfo.keys())[list(userinfo.values()).index(username)])
            #AccountsManager.remove_user(user_id)

            user_db=pd.read_csv("database/UserInfos.csv",index_col=0)
            user_db.loc[user_id,'usertype']='DeletedUser'
            user_db.to_csv("database/UserInfos.csv")

            selection = ordinary_list.curselection()
            ordinary_list.delete(selection[0])

            # final output
            print("Removed {} from the system.".format(username))

            #for id,name in userinfo:
            #    if name==username:
            #        user_id=id
            #print(user_id)
