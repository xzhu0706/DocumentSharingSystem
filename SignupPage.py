import tkinter as tk
import AccountsManager

class SignupPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        #LABELS
        label_type = tk.Label(self, text="® FourOfUS 2018", fg = "gray",font=controller.footer_font)
        label = tk.Label(self, text="ShareWithMe")
        label.config(font=("Courier", 35, 'bold'))
        label_name = tk.Label(self, text="Name")
        label_email = tk.Label(self, text="Email")
        label_phone = tk.Label(self, text="Phone Number")
        label_password = tk.Label(self, text="Password")
        label_tech_interest = tk.Label(self, text="Technical Interest")
        
        #ENTRIES
        entry_name = tk.Entry(self)
        entry_email = tk.Entry(self)
        entry_phone = tk.Entry(self)
        entry_password = tk.Entry(self,show='*')
        entry_tech_interest = tk.Entry(self)

        #BUTTONS
        button_back = tk.Button(self, text="Back",command=lambda:controller.show_frame("MainPage"))
        button_signup = tk.Button(self, text="Sign Up",
                            command=lambda: self.sign_up(entry_name.get(),
                                                    entry_password.get(),
                                                    entry_tech_interest.get()))
    
        n = 150
        m = 25
        
        ##PLACING THE LABELS
        label_type.pack(side=tk.BOTTOM)
        label.pack(side=tk.TOP,ipady=20)
        label_name.place(x=n, y=m*5)
        label_email.place(x=n, y=m*7)
        label_phone.place(x=n, y=m*9)
        label_password.place(x=n, y=m*11)
        label_tech_interest.place(x=n, y=m*13)
        
        ##PLACING THE ENTRIES
        entry_name.place(x=n+125, y=m*5)
        entry_email.place(x=n+125, y=m*7)
        entry_phone.place(x=n+125, y=m*9)
        entry_password.place(x=n+125, y=m*11)
        entry_tech_interest.place(x=n+125, y=m*13)
        
        ##PLACING THE BUTTONS
        button_back.place(x=250,y=380)
        button_signup.place(x=350,y=380)

    def sign_up(self, user_name, user_password, tech_interest):
        '''This is the function called when "sign up" is clicked'''

        # Check if all fields are filled
        if user_name == '' or user_password == '' or tech_interest == '':
            tk.messagebox.showerror("", "Please fill out all the fields!")
            return

        # Check if username already existed in pending applications
        if AccountsManager.is_pending(user_name):
            tk.messagebox.showerror("Error", "You application is still pending, please wait for approval!")
            return

        # Check if username already existed in accounts db
        if AccountsManager.username_exists(user_name):
            tk.messagebox.showerror("Error", "User name already existed, please re-enter!")
            return

        # Add account application to db
        AccountsManager.add_pending_user({
            'username': user_name,
            'password': user_password,
            'technical_interest': tech_interest
        })
        tk.messagebox.showinfo("Information", "Registration is successful, please wait for approval.")
        self.controller.show_frame("MainPage")
