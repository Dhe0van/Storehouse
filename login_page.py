import tkinter as tk
from PIL import Image, ImageTk

class LoginPage(tk.Frame):
        
    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.settings = main_window.settings

        # Properties
        self.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Frames
        self.create_container_frame()
        self.create_title()
        self.create_entry_fields()
        self.create_warning_message()
        self.create_verify_button()

    def create_container_frame(self):
        self.container_frame = tk.Frame(self, bg="white")
        self.container_frame.pack(fill="both", expand=True)

    def create_title(self):
        # self.title = tk.Label(self.container_frame, font=("Monsterrat", 45), text="Storehouse", bg="white")
        # self.title.pack(pady=60)
        # Image Logo Header
        image = Image.open(self.settings.logo)
        image_w, image_h = image.size
        ratio = image_w/(self.settings.width//10)
        image_new_size = (int(image_w/ratio), int(image_h/ratio))        
        image = image.resize(image_new_size)
        self.logo_header = ImageTk.PhotoImage(image)
        self.logo_label = tk.Label(self.container_frame, image=self.logo_header, bd=0)
        self.logo_label.pack(pady=(70, 30))


    def create_entry_fields(self):
        self.username_label_frame = tk.LabelFrame(self.container_frame, width=self.settings.width//6, height=self.settings.height//4, font=("Monsterrat", 12), text="Username:", bg="white", bd=0)
        self.username_label_frame.pack()

        self.username = tk.StringVar()
        self.username_field = tk.Entry(self.username_label_frame, width=30, font=("Monsterrat", 15), textvariable=self.username)
        self.username_field.pack(padx=10, pady=10)

        self.password_label_frame = tk.LabelFrame(self.container_frame, width=self.settings.width//6, height=self.settings.height//4, font=("Monsterrat", 12), text="Password:", bg="white", bd=0)
        self.password_label_frame.pack(pady=20)

        self.password = tk.StringVar()
        self.password_field = tk.Entry(self.password_label_frame, width=30, font=("Monsterrat", 15), textvariable=self.password, show="*")
        self.password_field.pack(padx=10, pady=10)

    def create_warning_message(self):
        self.warning_message = tk.Label(self.container_frame, font=("Monsterrat", 14), bg="white", fg="red")
        self.warning_message.pack()

    def create_verify_button(self):
        self.verify_button = tk.Button(self.container_frame, width=10, height=2, font=("Monsterrat", 20), text="Verify", bg="white", activebackground="white", command=self.main_window.verify_auth)
        self.verify_button.pack(pady=60)
