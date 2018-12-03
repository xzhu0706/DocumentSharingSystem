from PIL import ImageTk, Image
from DocumentViewerPage import *
import speech_recognition as sr


class DocumentEditorPage(DocumentViewerPage):

    def __init__(self, parent, controller):

        super(DocumentEditorPage, self).__init__(parent, controller)

        speech_recognition_button = tk.Button(self, fg="red", text="Speech Recognition",
                                              command=self.speech_recognition)

        update_button = tk.Button(self, text="Update")  # ,command=lambda:)
        lock_button = tk.Button(self, text="Lock")  # ,command=lambda:)

        unlock_button = tk.Button(self, text="Unlock")  # ,command=lambda:)
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