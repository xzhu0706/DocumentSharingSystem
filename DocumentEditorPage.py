#from PIL import ImageTk, Image
from DocumentViewerPage import *
import speech_recognition as sr
import pandas as pd


class DocumentEditorPage(DocumentViewerPage):

    def __init__(self, parent, controller):

        super(DocumentEditorPage, self).__init__(parent, controller)

        speech_recognition_button = tk.Button(self, fg="red", text="Speech Recognition",
                                              command=self.speech_recognition)

        update_button = tk.Button(self, text="Update", command=self.update_doc)
        lock_button = tk.Button(self, text="Lock", command=self.lock_doc)
        unlock_button = tk.Button(self, text="Unlock", command=self.unlock_doc)
        logout_button = tk.Button(self, text="Log Out", fg="blue", command=lambda: controller.show_frame("MainPage"))

        n = 150
        m = 50

        update_button.place(x=n + 325, y=m * 3)
        lock_button.place(x=n + 325, y=m * 4)
        unlock_button.place(x=n + 325, y=m * 5)
        logout_button.place(x=n + 380, y=m - 20)
        speech_recognition_button.place(x=n, y=m * 10 + 20)

        # Check taboo words in title if document is just created
        if self.doc_info['current_seq_id'] == '-':
            self.update_check()

    def speech_recognition(self):
        r = sr.Recognizer()
        print('start speech')
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            # print(r.recognize_google(audio))
            content = r.recognize_google(audio).split()
            for word in content:
                self.content.insert(tk.CURRENT, word + '\n')
        except Exception as e:
            tk.messagebox.showerror("Error", "Could not request results from Google \
                Speech Recognition service; {0}".format(e))

    def lock_doc(self):
        if DocumentsManager.lock_doc(self.userid, self.docid):
            tk.messagebox.showinfo("", "You have successfully locked the document!")
        else:
            tk.messagebox.showerror("", "Fail to lock the document because it's been locked by someone else!")

    def unlock_doc(self):
        if DocumentsManager.unlock_doc(self.userid, self.docid):
            tk.messagebox.showinfo("", "You have successfully unlocked the document!")
        else:
            tk.messagebox.showerror("", "You cannot unlock a document unless you have locked it first!")

    def update_doc(self):
        if DocumentsManager.is_locker(self.userid, self.docid):
            updated_content = {
                'title': self.title.get(1.0, 'end-1c'),
                'content': self.content.get(1.0, 'end-1c')
            }
            DocumentsManager.update_doc(self.userid, self.docid, updated_content)
            # tk.messagebox.showinfo("", "You have successfully updated the document! Please unlock if you are done.")
            self.update_check()
        else:
            tk.messagebox.showerror("", "Fail to update the document because you did not lock the document.")

    def update_check(self):
        taboo_list = self.get_taboo_words()
        words_used = self.title.get(1.0, 'end-1c').split()
        content_words = self.content.get(1.0, 'end-1c').split('\n')
        words_used.extend(content_words)
        # empty list to store taboo words used
        taboo_used = []
        # checking if any taboo words in the content
        for word in words_used:
            if word in taboo_list:
                # add the word to the used taboo word list
                taboo_used.append(word)
        # if any taboo words found
        if len(taboo_used) > 0:
            # add user to warning list
            DocumentsManager.add_warning(self.userid, self.docid)
            tk.messagebox.showwarning("", "Updated sucessfully. Following taboo words were used: {}.\nPlease fix them ASAP!".format(taboo_used))
        else:
            tk.messagebox.showinfo("", "You have successfully updated the document! Please unlock if you are done.")


    def updateCheck(self):
        # might need to check if it
        # reading the Documents.csv file

        document_db = pd.read_csv("database/Documents.csv", delimiter=',')
        # gettig the opened document id
        doc_id = self.controller.opened_docid
        # making a list of all the documents ID in the Documents.csv
        # so that we can find the index of the opened docuemnt
        doc_id_list = list(document_db._getitem_column('doc_id'))
        # making a list of all the contents of the Documents.csv
        doc_content_list = list(document_db._getitem_column('title'))
        # finding in which index our opened document is
        index_of_doc_id = doc_id_list.index(doc_id)
        # getting content of the opened document
        this_document = list(doc_content_list[index_of_doc_id].split())
        # reading the TabooWords.csv file
        tabbo_db = pd.read_csv("database/TabooWords.csv", delimiter=',')
        # making a list of all taboo words
        tabboo_list = list(tabbo_db._getitem_column('word'))
        # empty list to store taoo words found
        tabboo_used = []

        # checking if any taboo words in the content
        for i in tabboo_list:
            if i in this_document:
                # add the word to the found taboo word list
                tabboo_used.append(i)
                # if any taboo words found
        if len(tabboo_used) > 0:
            tk.messagebox.showerror("Error","Update unsucessful\nFollowing taboo words used: \n{}".format(tabboo_used))
        else:
            tk.messagebox.showinfo("Information","Successfully updated")
