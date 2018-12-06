from DocumentEditorPage import *

class DocumentOwnerPage(DocumentEditorPage):

    def __init__(self, parent, controller):

        super(DocumentOwnerPage, self).__init__(parent, controller)
        

        manage_contributor_button = tk.Button(self, text="Manage Contributors")#,command=lambda:)

        OPTIONS = [
            "Private",
            "Shared",
            "Restricted",
            "Public"
        ]
        variable = tk.StringVar(self)
        variable.set("Scopes")

        # DROP DOWN
        # REFRENE FOR DROP DOWN
        '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
        scopes_drop_down = tk.OptionMenu(self, variable, *OPTIONS)

        n = 150
        m = 50

        manage_contributor_button.place(x=n+325, y=m*6)
        scopes_drop_down.place(x=n+325, y=m+50)


# class DocumentPage(tk.Frame):
#
#     def __init__(self, parent, controller):
#
#         self.username = controller.get_username()
#         self.docid = controller.get_docid()
#
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label_type = tk.Label(self, text="® FourofUS 2018", fg = "gray",font=controller.footer_font)
#         label1 = tk.Label(self, text="ShareWithME")
#         label1.config(font=("Courier", 35, 'bold'))
#         label_title = tk.Label(self, text="Title")
#         label_content = tk.Label(self, text="Content")
#         self.title = Text(self, height=1, width=30, highlightbackground="black", highlightcolor="black", highlightthickness=1,
#                           font=("Times New Roman", 18))
#         self.content = Text(self, height=25, width=60, highlightbackground="black", highlightcolor="black", highlightthickness=1,)
#         #need to save everythin in it lets after 10 sec
#         # content.insert(CURRENT,"HellO")
#
#         OPTIONS = [
#                    "Version 3",
#                    "Version 2",
#                    "Version 1"
#                    ] #etc
#         variable = StringVar(self)
#         variable.set("All versions")
#
#         #DROP DOWN
#         ##REFRENE FOR DROP DOWN
#         '''https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534'''
#         #need to be replaced by the bakend data
#         versions_drop_down = OptionMenu(self, variable, *OPTIONS)
#
#         speech_recognition_button = tk.Button(self, fg="red", text="Speech Recognition", command=self.speech_recognition)
#
#         update_button = tk.Button(self, text="Update")#,command=lambda:)
#         lock_button = tk.Button(self, text="Lock")#,command=lambda:)
#
#         unlock_button = tk.Button(self, text="Unlock" )#,command=lambda:)
#         logout_button = tk.Button(self, text="Log Out", fg="blue", command=lambda: controller.show_frame("MainPage"))
#
#         add_contributor_button = tk.Button(self, text="Manage Contributors")#,command=lambda:)
#
#         complain_button = tk.Button(self, text="Complain")#,command=lambda:)
#         back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(controller.get_usertype())) # jump back to user page
#
#
#         n = 150
#         m = 50
#
#         label_type.pack(side=BOTTOM)
#         label1.pack(side=TOP, ipady=20)
#         label_title.place(x=n-120, y=m+10)
#         self.title.place(x=n-120, y=m+30)
#         label_content.place(x=n-120, y=m+70)
#         self.content.place(x=n-120, y=m+90)
#         versions_drop_down.place(x=n+325,y=m+20)
#
#         update_button.place(x=n+325, y=m*3)
#         lock_button.place(x=n+325, y=m*4)
#         unlock_button.place(x=n+325, y=m*5)
#         logout_button.place(x=n+380, y=m-20)
#         add_contributor_button.place(x=n+325, y=m*6)
#         complain_button.place(x=n+325, y=m*7)
#         back_button.place(x=n+325, y=m*8)
#         speech_recognition_button.place(x=n, y=m * 10 + 20)
#
#
#     def speech_recognition(self):
#         r = sr.Recognizer()
#
#         print('start speech')
#
#         with sr.Microphone() as source:
#             audio = r.listen(source)
#         try:
#             # print(r.recognize_google(audio))
#             content = r.recognize_google(audio).split()
#             for word in content:
#                 self.content.insert(CURRENT, word + '\n')
#                 print(word)
#         except Exception as e:
#             print("Could not request results from Google \
#                 Speech Recognition service; {0}".format(e))
