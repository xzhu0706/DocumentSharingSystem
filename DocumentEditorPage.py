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
        logout_button = tk.Button(self, text="Log Out", fg="blue", command=lambda: controller.log_out())

        n = 150
        m = 50

        update_button.place(x=n + 325, y=m * 3)
        lock_button.place(x=n + 325, y=m * 4)
        unlock_button.place(x=n + 325, y=m * 5)
        logout_button.place(x=n + 380, y=m - 20)
        speech_recognition_button.place(x=n - 120, y=m * 10 + 20)

        # # Check taboo words in title if document was just created
        # if self.doc_info['current_seq_id'] == '-':
        #     self.update_check()

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
            self.fetch_status()
        else:
            tk.messagebox.showerror("", "Fail to lock the document because it's been locked!")

    def unlock_doc(self):
        if DocumentsManager.unlock_doc(self.userid, self.docid, self.controller.is_su()):
            tk.messagebox.showinfo("", "You have successfully unlocked the document!")
            self.fetch_status()
        else:
            tk.messagebox.showerror("", "You cannot unlock a document unless you have locked it first!")

    def update_doc(self):
        # TODO: might need to prevent saving UNK into db, instead we want the original words to be saved
        if DocumentsManager.is_locker(self.userid, self.docid):
            updated_content = {
                'title': self.title.get(1.0, 'end-1c'),
                'content': self.content.get(1.0, 'end-1c')
            }
            DocumentsManager.update_doc(self.userid, self.docid, updated_content)
            # tk.messagebox.showinfo("", "You have successfully updated the document! Please unlock if you are done.")
            self.update_check()
            self.refresh_content()
        else:
            tk.messagebox.showerror("", "Fail to update the document because you did not lock the document.")

    def update_check(self):
        taboo_list = self.get_taboo_words()
        words_used = self.title.get(1.0, tk.END).split()
        content_words = self.content.get(1.0, tk.END).split('\n')
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
            AccountsManager.add_warning(self.userid, self.docid)
            tk.messagebox.showwarning("", "Updated sucessfully. Following taboo words were used: {}.\nPlease fix them ASAP!".format(taboo_used))
        else: #if self.doc_info['current_seq_id'] != '-':
            tk.messagebox.showinfo("", "You have successfully updated the document! Please unlock if you are done.")

