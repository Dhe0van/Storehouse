import tkinter as tk

class AddWindow(tk.Toplevel):
        
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.settings = main_window.settings

        self.title(self.settings.add_window_title)
        self.geometry(self.settings.add_window_screen)
        self.resizable(False, False)

        self.create_main_frame()
        self.create_title()
        self.create_fields()
        self.create_warningMessage()
        self.create_verify_buttons()

    def create_main_frame(self):
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(fill="both", expand=True)

    def create_title(self):
        title_frame = tk.Frame(self.main_frame, width=self.settings.add_window_width, height=self.settings.add_window_height//5, bg="white", bd=10)
        title_frame.pack(padx=7, pady=(7, 0))
        title = tk.Label(title_frame, width=self.settings.add_window_width, height=self.settings.add_window_height//250, font=("Monsterrat", 35), text="ADD NEW PRODUCT", bg="white")
        title.pack()

    def create_fields(self):
        desc_labelFrame = tk.LabelFrame(self.main_frame, width=self.settings.add_window_width, height=2*self.settings.add_window_height//4, font=("Monsterrat", 13), text="Product Description", bg="white")
        desc_labelFrame.pack()
        self.fields = []

        labels = [
                ["Name", ':'],
                ["Code", ':'],
                ["Price", ':'],
                ["Total", ':'],
                ["Type", ':'],
                ["Expired", ':']
                ]
        self.field_vars = [
                {"name" : tk.StringVar()},
                {"code" : tk.StringVar()},
                {"price" : tk.StringVar()},
                {"total" : tk.StringVar()},
                {"type" : tk.StringVar()},
                {"expired" : tk.StringVar()},
                ]

        rows, columns = len(labels), len(labels[0])
        self.add_table_label = []
        for row in range(rows):
            a_row = []
            for column in range(columns):
                if column == 0:
                    label = tk.Label(desc_labelFrame, font=("Monsterrat", 18), text=labels[row][0], bg="white")
                    label.grid(row=row, column=0, sticky='w', pady=(0, 20))
                    a_row.append(label)
                elif column == 1:
                    equal = tk.Label(desc_labelFrame, font=("Monsterrat", 18), text=':', bg="white")
                    equal.grid(row=row, column=1, padx=10, pady=(0, 20))
                    a_row.append(equal)
            self.add_table_label.append(a_row)

        row = 0
        self.add_table_fields = []
        for name_and_var in self.field_vars:
            for name in name_and_var:
                field = tk.Entry(desc_labelFrame, font=("Monsterrat", 17), width=20, textvariable=self.field_vars[row][name])
                field.grid(row=row, column=2, sticky='e', padx=(100, 10), pady=(0, 20))
                self.add_table_fields.append(field)
                break
            row += 1

    def create_warningMessage(self):
        self.warning_message = tk.Label(self.main_frame, font=("Monsterrat", 12), bg="white", fg="red")
        self.warning_message.pack()

    def create_verify_buttons(self):
        verify_button_frame = tk.Frame(self.main_frame, width=self.settings.add_window_width, height=self.settings.height, bg="white")
        verify_button_frame.pack()

        self.cancel_button = tk.Button(verify_button_frame, width=10, height=2, font=("Monsterrat", 14), text="Cancel", bg="white", highlightbackground="black", bd=0, command=self.destroy)
        self.cancel_button.grid(row=0, column=0, padx=(0, 20), pady=(40, 0))

        self.reset_button = tk.Button(verify_button_frame, width=10, height=2, font=("Monsterrat", 14), text="Reset", bg="white", highlightbackground="black", bd=0, command=lambda:self.reset_entry_field(self.add_table_fields))
        self.reset_button.grid(row=0, column=1, padx=(0, 0), pady=(40, 0))

        self.confirm_button = tk.Button(verify_button_frame, width=10, height=2, font=("Monsterrat", 14), text="Confirm", bg="white", highlightbackground="black", bd=0, command=self.confirm)
        self.confirm_button.grid(row=0, column=2, padx=(20, 0), pady=(40, 0))

    def reset_entry_field(self, fields):
        for field in fields:
            field.delete(0, "end")

    def confirm(self):
        items = self.settings.items_data

        name = self.field_vars[0]["name"].get().title()
        code = self.field_vars[1]["code"].get().upper()
        price = self.field_vars[2]["price"].get()
        total = self.field_vars[3]["total"].get()
        type = self.field_vars[4]["type"].get().title()
        expired = self.field_vars[5]["expired"].get()

        # Checking the condition of entry field whether it is empty or not
        filled = bool(name and code and price and total and type and expired)
        if filled:
            new_item = {
                    name : {
                        "code" : code,
                        "price" : price,
                        "total" : total,
                        "type" : type,
                        "expired" : expired
                        }
                    }
            items.append(new_item)
            self.settings.save_items_data(self.settings.items_loc, items)
            self.main_window.pages["main_app"].items_listbox.insert("end", name)
            last_index = self.main_window.pages["main_app"].item_indexs[-1]
            self.main_window.pages["main_app"].item_indexs.append(last_index+1)
            self.destroy()
        else:
            self.warning_message.configure(text="Please fill all entry fields first before adding a new product!")
