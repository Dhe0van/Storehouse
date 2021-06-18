import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from math import sqrt

class MainPage(tk.Frame):
        
    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.settings = main_window.settings

        # Flag
        self.items = self.settings.items_data
        self.first_item = self.settings.items_data[0]
        self.last_current_item_index = 0
        self.change_mode = False
        self.item_indexs = []

        # Properties
        self.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Frames
        self.create_left_frame()
        self.create_right_frame()
        self.configure_frames()

    def create_left_frame(self):
        self.left_frame = tk.Frame(self, bg="white")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.create_left_header()
        self.create_left_content()

    def create_left_header(self):
        self.left_header_frame = tk.Frame(self.left_frame, bg="black", width=self.settings.width//4, height=self.settings.height//3)
        self.left_header_frame.pack()

        # Image Logo Header
        image = Image.open(self.settings.logo)
        image_w, image_h = image.size
        ratio = image_w/(self.settings.width//sqrt(40.8))
        image_new_size = (int(image_w/ratio), int(image_h/ratio))        
        image = image.resize(image_new_size)
        self.logo_header = ImageTk.PhotoImage(image)
        self.logo_label = tk.Label(self.left_header_frame, image=self.logo_header, bd=0)
        self.logo_label.pack()

        # Add, Remove, Search
        self.action_frame = tk.Frame(self.left_header_frame, width=self.settings.width//7, height=self.settings.height//20, bg="white")
        self.action_frame.pack(fill='x')

        self.add_button = tk.Button(self.action_frame, font=("", 20), text='+', bg="white", fg="black", command=self.main_window.create_new_addWindow)
        self.add_button.grid(row=0, column=0, padx=(0, 10))

        self.search_var = tk.StringVar()
        self.searchbox = tk.Entry(self.action_frame, bg="white", fg="black", font=("Monsterrat", 20), textvariable=self.search_var)
        self.searchbox.grid(row=0, column=1, padx=20)

        self.find_button = tk.Button(self.action_frame, font=("", 20), text="🔍", bg="white", fg="light green", command=self.search_item_inListbox)
        self.find_button.grid(row=0, column=2)

    def search_item_inListbox(self):
        items = self.items
        item_searched = self.search_var.get().lower()

        if item_searched:
            self.item_indexs = []
            item_index = 0

            for item in items:
                for name, desc in item.items():
                    if item_searched in name.lower():
                        self.item_indexs.append(item_index)
                item_index += 1

            self.items_listbox.delete(0, "end")
            self.show_item()
        else:
            self.show_all_items_in_listbox()

    def show_item(self):
        items = self.items
        for index in self.item_indexs:
            item = items[index]
            for name in item:
                self.items_listbox.insert("end", name)

    def show_all_items_in_listbox(self):
        self.items_listbox.delete(0, "end")
        self.item_indexs = []
        items = self.items
        item_index = 0
        for item in items:
            self.item_indexs.append(item_index)
            item_index += 1
        self.show_item()

    def create_left_content(self):
        self.left_content_frame = tk.Frame(self.left_frame, width=self.settings.width//4, height=self.settings.height//2, bg="white")
        self.left_content_frame.pack(fill="both")

        # List Box (contain list of items)
        self.items_listbox = tk.Listbox(self.left_content_frame, height=self.settings.height//2, bg="white", fg="black", font=("Monsterrat", 20))
        self.items_listbox.pack(side="left", fill="both", expand=True)

        # Scroll Bar
        self.scrollbar = tk.Scrollbar(self.left_content_frame)
        self.scrollbar.pack(side="right", fill='y')

        # Putting a list of data into the listbox
        self.show_all_items_in_listbox()

        # Connecting scrollbar into listbox
        self.items_listbox.configure(yscrollcommand=self.scrollbar.set) # set to the listbox
        self.scrollbar.configure(command=self.items_listbox.yview) # Changing the view of listbox into corresponding y value whenever dragged by cursor

        self.items_listbox.bind("<<ListboxSelect>>", self.clicked_item_in_itemListbox)

    def clicked_item_in_itemListbox(self, event):
        if not self.change_mode:
            selection = event.widget.curselection()
            try:
                clicked_item_index = selection[0]
                self.last_current_item_index = clicked_item_index
            except IndexError:
                clicked_item_index = self.last_current_item_index
            index = self.item_indexs[clicked_item_index]
            self.last_current_item_index = index

            current_item = self.items[index]

            for item_name, item_desc in current_item.items():
                code = item_desc["code"]
                price = item_desc["price"]
                total = item_desc["total"]
                type_of_item = item_desc["type"]
                expired = item_desc["expired"]

                self.right_header_label.configure(text=item_name.title())
                self.table_desc[0][1].configure(text=code)
                self.table_desc[1][1].configure(text=price)
                self.table_desc[2][1].configure(text=total)
                self.table_desc[3][1].configure(text=type_of_item)
                self.table_desc[4][1].configure(text=expired)

    def create_right_frame(self):
        self.right_frame = tk.Frame(self, bg="white", width=self.settings.width//4)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.create_right_header()
        self.create_right_content()

    def create_right_header(self):
        self.right_header_frame = tk.Frame(self.right_frame, width=self.settings.width//3, height=self.settings.height//7, bg="white")
        self.right_header_frame.pack(fill='x')

        self.first_item_name = list(self.first_item.keys())[0].title()
        self.right_header_label = tk.Label(self.right_header_frame, font=("Monsterrat", 55), text=self.first_item_name, bg="white", fg="black")
        self.right_header_label.pack(pady=121)

    def create_right_content(self):
        self.right_content_frame = tk.Frame(self.right_frame, width=self.settings.width//3, height=6*self.settings.height//7, bg="white", highlightbackground="black", highlightthickness=1)
        self.right_content_frame.pack(fill="both", expand=True)

        # Prototype
        item_desc = []
        for desc in list(self.first_item.values()):
            item_desc = [
                    ["Code:", desc["code"]],
                    ["Price:", desc["price"]],
                    ["Total:", desc["total"]],
                    ["Type:", desc["type"]],
                    ["Expired:", desc["expired"]]
                    ]
        self.table_desc = []
        rows, columns = len(item_desc), len(item_desc[0])
        for row in range(rows):
            a_row = [] # Using a 2D array in here because tkinter only tolerate using it (it will error if you just using 1D array)
            for column in range(columns):
                if column == 0: # For the type of description
                    desc_key = tk.Label(self.right_content_frame, font=("Monsterrat", 20), text=item_desc[row][0], bg="white", fg="black")
                    a_row.append(desc_key)
                    desc_key.grid(sticky='w', padx=(30, 0))
                elif column == 1: # For the value of type
                    desc_value = tk.Label(self.right_content_frame, font=("Monsterrat", 30), text=item_desc[row][1], bg="white", fg="black")
                    a_row.append(desc_value)
                    desc_value.grid(sticky='w', padx=(50, 0), pady=(0, 20))
            self.table_desc.append(a_row)

        self.change_button = tk.Button(self.right_content_frame, width=10, height=2, font=("Monsterrat", 25), text="Change", bg="white", fg="black", highlightbackground="black", bd=0, command=self.change_item)
        self.change_button.grid(row=10, column=0, padx=(550, 0), sticky="nsew")

        self.remove_button = tk.Button(self.right_content_frame, width=3, height=2, font=("", 25), text='🗑', bg="white", fg="red", command=self.remove_item)
        self.remove_button.grid(row=10, column=1, padx=(500, 0), sticky='e')

        # For update
        self.cancel_change_button = tk.Button(self.right_content_frame, width=8, height=2, font=("Monsterrat", 25), text="Cancel", bg="white", fg="black", highlightbackground="black", bd=0, command=self.cancel_changes)
        self.confirm_change_button = tk.Button(self.right_content_frame, width=8, height=2, font=("Monsterrat", 25), text="Confirm", bg="white", fg="black", highlightbackground="black", bd=0, command=self.confirm_changes)

    def remove_item(self):
        selected_item = self.last_current_item_index
        item_name = list(self.items[selected_item].keys())[0].title()

        confirmation = messagebox.askyesno(title="Remove Product", message=f"Are you sure to remove {item_name}?")
        if confirmation:
            self.item_indexs.pop(self.last_current_item_index)
            self.last_current_item_index = 0
            self.first_item = self.items[self.last_current_item_index]

            name = list(self.first_item.keys())[0]
            desc = self.first_item[name]
            self.right_header_label.configure(text=name)
            self.table_desc[0][1].configure(text=desc["code"])
            self.table_desc[1][1].configure(text=desc["price"])
            self.table_desc[2][1].configure(text=desc["total"])
            self.table_desc[3][1].configure(text=desc["type"])
            self.table_desc[4][1].configure(text=desc["expired"])

            self.items_listbox.delete(selected_item)
            self.items.pop(selected_item)
            self.settings.save_items_data(self.settings.items_loc, self.items)

    def mode_changed(self):
        if self.change_mode:
            self.add_button.configure(state="disabled")
            self.searchbox.configure(state="disabled")
            self.find_button.configure(state="disabled")
        else:
            self.add_button.configure(state="normal")
            self.searchbox.configure(state="normal")
            self.find_button.configure(state="normal")

    def change_item(self):
        self.change_mode = True
        self.mode_changed()
        selected_item = self.last_current_item_index

        self.change_button.grid_forget()
        self.remove_button.grid_forget()
        for row in range(5):
            self.table_desc[row][0].destroy()
            self.table_desc[row][1].destroy()

        item_desc = []
        name = None
        for name, desc in self.items[selected_item].items():
            item_desc = [
                    ["Code:", desc["code"]],
                    ["Price:", desc["price"]],
                    ["Total:", desc["total"]],
                    ["Type:", desc["type"]],
                    ["Expired:", desc["expired"]]
                    ]
        
        self.new_name = tk.StringVar()
        self.right_header_label.pack_forget()
        self.right_header_label = ttk.Entry(self.right_header_frame, width=20, font=("Monsterrat", 55), justify="center", textvariable=self.new_name)
        self.right_header_label.pack(pady=121)
        self.right_header_label.insert(0, name.title())

        self.field_vars = [
                {"code" : tk.StringVar()},
                {"price" : tk.StringVar()},
                {"total" : tk.StringVar()},
                {"type" : tk.StringVar()},
                {"expired" : tk.StringVar()},
                ]

        self.update_table_desc = []
        rows, columns = len(item_desc), len(item_desc[0])
        for row in range(rows):
            a_row = [] 
            for column in range(columns):
                if column == 0:
                    desc_key = tk.Label(self.right_content_frame, font=("Monsterrat", 20), text=item_desc[row][0], bg="white", fg="black")
                    a_row.append(desc_key)
                    desc_key.grid(sticky='w', padx=(30, 0))
                elif column == 1:
                    desc_entry = ttk.Entry(self.right_content_frame, font=("Monsterrat", 30), textvariable=self.field_vars[row][list(self.field_vars[row].keys())[0]])
                    desc_entry.insert(0, item_desc[row][column])
                    a_row.append(desc_entry)
                    desc_entry.grid(sticky='w', padx=(50, 0), pady=(0, 20))
            self.update_table_desc.append(a_row)

        self.cancel_change_button.grid(row=10, column=0, padx=(450, 100), sticky="nsew")
        self.confirm_change_button.grid(row=10, column=1, padx=(50, 100), sticky="nsew")

    def confirm_changes(self):
        selected_item = self.last_current_item_index

        name = self.new_name.get().title()
        code = self.field_vars[0]["code"].get().upper()
        price = self.field_vars[1]["price"].get()
        total = self.field_vars[2]["total"].get()
        type = self.field_vars[3]["type"].get().title()
        expired = self.field_vars[4]["expired"].get()

        filled = bool(name and code and price and total and type and expired)
        if filled:
            changed_item = {
                        name : {
                            "code" : code,
                            "price" : price,
                            "total" : total,
                            "type" : type,
                            "expired" : expired
                            }
                        }

            self.items[selected_item] = changed_item
            self.settings.save_items_data(self.settings.items_loc, self.items)
            # self.items_listbox.delete(selected_item)
            # self.items_listbox.insert(selected_item, name)
            self.items_listbox.delete(0, "end")
            self.show_item()
            self.cancel_changes() # Change entry field to label just like cancel with an exception had been saved before.
        else:
            messagebox.showwarning(title=None, message="You have to fill all the Entry Field!")

    def cancel_changes(self):
        self.change_mode = False
        self.mode_changed()
        selected_item = self.last_current_item_index
       
        self.right_header_label.pack_forget()
        self.right_header_label = tk.Label(self.right_header_frame, font=("Monsterrat", 55), text=list(self.items[selected_item].keys())[0].title(), bg="white", fg="black")
        self.right_header_label.pack(pady=121)
        self.cancel_change_button.grid_forget()
        self.confirm_change_button.grid_forget()
        for row in range(5):
            self.update_table_desc[row][0].destroy()
            self.update_table_desc[row][1].destroy()

        item_desc = []
        for desc in list(self.items[selected_item].values()):
            item_desc = [
                    ["Code:", desc["code"]],
                    ["Price:", desc["price"]],
                    ["Total:", desc["total"]],
                    ["Type:", desc["type"]],
                    ["Expired:", desc["expired"]]
                    ]
        self.table_desc = []
        rows, columns = len(item_desc), len(item_desc[0])
        for row in range(rows):
            a_row = [] # Using a 2D array in here because tkinter only tolerate using it (it will error if you just using 1D array)
            for column in range(columns):
                if column == 0: # For the type of description
                    desc_key = tk.Label(self.right_content_frame, font=("Monsterrat", 20), text=item_desc[row][0], bg="white", fg="black")
                    a_row.append(desc_key)
                    desc_key.grid(sticky='w', padx=(30, 0))
                elif column == 1: # For the value of type
                    desc_value = tk.Label(self.right_content_frame, font=("Monsterrat", 30), text=item_desc[row][1], bg="white", fg="black")
                    a_row.append(desc_value)
                    desc_value.grid(sticky='w', padx=(50, 0), pady=(0, 20))
            self.table_desc.append(a_row)

        self.change_button = tk.Button(self.right_content_frame, width=10, height=2, font=("Monsterrat", 25), text="Change", bg="white", fg="black", highlightbackground="black", bd=0, command=self.change_item)
        self.change_button.grid(row=10, column=0, padx=(550, 0), sticky="nsew")

        self.remove_button = tk.Button(self.right_content_frame, width=3, height=2, font=("", 25), text='🗑', bg="white", fg="red", command=self.remove_item)
        self.remove_button.grid(row=10, column=1, padx=(500, 0), sticky='e')

    def configure_frames(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=666) # The width got affected by self.right_header_label so the weight need to be increased
        # Why the Number is SO BIG!? Because when an item in the Listbox is selected the padx is pushing the self.right_content_frame and it will become ugly transition
        # If you don't get it just change the number to 1 or 2 (At least it works)
