import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from OrdinaryUser import *

class SuperUser(OrdinaryUser):

    def __init__(self, parent, controller):

        super(SuperUser, self).__init__(parent, controller)

        update_membership_button = tk.Button(self, text="Manage Membership")  # ,command=lambda:TO BE IMPLEMENTED BY BACKEND, can update or remove user
        taboo_words_button = tk.Button(self, text="Manage Taboo Words")  # ,command=lambdaTO BE IMPLEMENTED BY BACKEND

        # PLACING THE LABELS
        n = 150
        m = 50

        update_membership_button.place(x=n + 300, y=m * 8.5)
        taboo_words_button.place(x=n + 300, y=m * 9)

