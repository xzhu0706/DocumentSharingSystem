#from PIL import ImageTk, Image
from DocumentViewerPage import *
import speech_recognition as sr
import pandas as pd


class DocumentEditorPage(DocumentViewerPage):

    def __init__(self, parent, controller):


        super(DocumentEditorPage, self).__init__(parent, controller)


        speech_recognition_button = tk.Button(self, fg="red", text="Speech Recognition",
                                              command=self.speech_recognition)

        update_button = tk.Button(self, text="Update",command=lambda: self.updateCheck())
        lock_button = tk.Button(self, text="Lock")#,command=lambda:self.locker())

        unlock_button = tk.Button(self, text="Unlock")# ,command=lambda:self.unlocker())
        logout_button = tk.Button(self, text="Log Out", fg="blue", command=lambda: controller.show_frame("MainPage"))

        n = 150
        m = 50

        update_button.place(x=n + 325, y=m * 3)
        lock_button.place(x=n + 325, y=m * 4)
        unlock_button.place(x=n + 325, y=m * 5)
        logout_button.place(x=n + 380, y=m - 20)
        speech_recognition_button.place(x=n, y=m * 10 + 20)

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


    def updateCheck(self):
        # reading the Documents.csv file

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
        this_document= list(doc_content_list[index_of_doc_id].split())
        row=DocumentsManager.get_doc_info(doc_id)
        if (row['is_locked']==False):
            print("suces")

        # reading the TabooWords.csv file
        tabbo_db=pd.read_csv("database/TabooWords.csv", delimiter=',')
        # making a list of all taboo words
        tabboo_list=list(tabbo_db._getitem_column('word'))
        # empty list to store taoo words found
        tabboo_used=[]

        # checking if any taboo worsd in the content
        for i in tabboo_list:
            if i in this_document:
                # add the word to the found taboo word list
                tabboo_used.append(i)
                # if any taboo words found
        if(len(tabboo_used)>0):
            tk.messagebox.showerror("Error","Update unsucessful\nFollowing taboo words used \n{}".format(tabboo_used))
        else:
            tk.messagebox.showinfo("Information","Successfully updated")
