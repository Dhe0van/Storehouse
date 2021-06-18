import tkinter as tk
from datetime import datetime as dt

from settings import Settings
from main_page import MainPage
from add_window import AddWindow
from login_page import LoginPage

class MainWindow(tk.Tk):
        
    def __init__(self, App):
        super().__init__()
        # Path
        self.storehouse = App 
        self.settings = App.settings

        # Properties
        self.title(self.settings.title)
        self.geometry(self.settings.screen)

        # Page
        self.create_container()
        self.pages = {}
        self.create_pages()

    def create_container(self):
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

    def create_pages(self):
        self.pages["main_app"] = MainPage(self.container, self)
        self.pages["login_page"] = LoginPage(self.container, self)

    def create_new_addWindow(self): # New secondary window for adding item to the Listbox
        add_window = AddWindow(self)
        add_window.mainloop() # The same as run method in the Storehouse class

    def change_page(self, page):
        raised_page = self.pages[page]
        raised_page.tkraise()

    def not_verified(self, current_hour, current_minute):
            id = self.settings.id
            inserted_username = self.pages["login_page"].username.get()
            inserted_password = self.pages["login_page"].password.get()
            verified = False

            if inserted_username in id:
                if inserted_password == id[inserted_username]:
                    verified = True
                    self.change_page("main_app")
                    new_login_time = {
                            "last_login" : {
                                "hour" : current_hour,
                                "minute" : current_minute,
                                "verified" : verified
                                }
                            }
                    self.settings.save_items_data(self.settings.last_login_loc, new_login_time)
                else:
                    self.pages["login_page"].warning_message.configure(text=f"The Password is wrong!")
            else:
                if bool(inserted_username) == True:
                    self.pages["login_page"].warning_message.configure(text=f"There is no username with {inserted_username}")
            new_login_time = {
                    "last_login" : {
                        "hour" : current_hour,
                        "minute" : current_minute,
                        "verified" : verified
                        }
                    }
            self.settings.save_items_data(self.settings.last_login_loc, new_login_time)


    def verify_auth(self):
        last_hour, last_minute = self.settings.last_login["last_login"]["hour"], self.settings.last_login["last_login"]["minute"]
        current_hour, current_minute = dt.now().hour, dt.now().minute
        verified = self.settings.last_login["last_login"]["verified"]

        # If user is logged in 5 minutes ago and it is verified.
        if (current_hour != last_hour) or (current_minute-last_minute > 5):
            self.not_verified(current_hour, current_minute)
        else:
            if verified:
                new_login_time = {
                        "last_login" : {
                            "hour" : current_hour,
                            "minute" : current_minute,
                            "verified" : verified
                            }
                        }
                self.settings.save_items_data(self.settings.last_login_loc, new_login_time)
                self.change_page("main_app")
            else:
                self.not_verified(current_hour, current_minute)

class Storehouse:
        
    def __init__(self):
        self.settings = Settings()
        self.main_window = MainWindow(self)
        self.main_window.verify_auth()

    def run(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    my_storehouse = Storehouse()
    my_storehouse.run()
