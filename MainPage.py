#############################################################################
#Name:MainPage.py
#Description: The page we see first when we run the program. We could log in,
#             sign up or exit the program in this page.
#############################################################################
import tkinter as tk
import AccountsManager

class MainPage(tk.Frame):

    # Constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #############
        #    GUI    #
        #############
        
        #LABLES
        label_type = tk.Label(self, text="® FourOfUS 2018", fg = "gray",font=controller.footer_font)
        label = tk.Label(self, text="ShareWithMe")
        label.config(font=("Courier", 45, 'bold'))
        label_name = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")
        
        #ENTRIES
        entry_name = tk.Entry(self)
        entry_password = tk.Entry(self, show='*')
        
        #BUTTONS
        button_signup = tk.Button(self, text="Sign Up",command=lambda: controller.show_frame("SignupPage"))
        button_login = tk.Button(self, text="Log In",command=lambda: self.log_in(entry_name.get(),
                                                                                entry_password.get()))
        button_guest = tk.Button(self, text="Guest User",command=lambda: controller.log_in_as_guest())
        #**********************
        #TODO: Need to work on this
        #**********************
        self.keep_login_var = tk.IntVar()
        checkbox_keep_login = tk.Checkbutton(self, text="Keep me logged in",
                                             variable=self.keep_login_var, fg="black")

        
        #CO-ORDINATES
        n = 150
        m = 50

        ##PLACING THE LABELS
        label_type.pack(side=tk.BOTTOM)
        label.pack(side=tk.TOP,ipady=50)
        label_name.place(x=n, y=m*4)
        label_password.place(x=n, y=m*5)
        
        ##PLACING THE ENTRIES
        entry_name.place(x=n+100, y=m*4)
        entry_password.place(x=n+100, y=m*5)
        
        ##PLACING THE BUTTON
        button_login.place(x=n+30,y=m*7)
        button_signup.place(x=n+130,y=m*7)
        button_guest.place(x=n+230,y=m*7)
        
        ##PLACING THE CHECKBOX
        checkbox_keep_login.place(x=n+100,y=m*6)


    # This function gets called when "log in" button is clicked.
    # It checks username and password in the file and takes the user
    # to the corresponding page depending on their user type.
    def log_in(self, username_input, password_input):

        # Check if all fields are filled
        if username_input == '' or password_input == '':
            tk.messagebox.showerror("Error", "Please fill out all the fields!")
            return

        # Check if username is in pending applications db
        if AccountsManager.is_pending(username_input):
            tk.messagebox.showerror("Error", "Your application is still pending!")
            return

        # Check if username exists in db, if yes then check password
        if not AccountsManager.username_exists(username_input):
            tk.messagebox.showerror("Error", "Wrong username!")
        else:
            user = AccountsManager.validate_user(username_input, password_input)
            if user:
                # If password match (validates successfully), set user info into the system by calling the controller method
                username = username_input
                userid = user['userid']
                usertype = user['usertype']
                self.controller.log_in(username, userid, usertype)
            else:
                tk.messagebox.showerror("Error", "Wrong password!")
