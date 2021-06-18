from json import load, dump

class Settings:
        
    def __init__(self):
        # Main Window Properties
        self.title = "Food Storehouse"
        base = 200
        ratio = (16, 9)
        self.width = base*ratio[0]
        self.height = base*ratio[1]
        self.screen = f"{self.width}x{self.height}"

        # Add Window Properties
        self.add_window_title = "Add"
        add_window_ratio = (3, 4)
        self.add_window_width = base*add_window_ratio[0]
        self.add_window_height = base*add_window_ratio[1]
        self.add_window_screen = f"{self.add_window_width}x{self.add_window_height}"

        # Location
        self.logo = "img/logo.jpeg"
        self.items_loc = "storage/items.json"
        self.id_loc = "storage/id.json"
        self.last_login_loc = "storage/last_login.json"
        self.load_item_data()
        self.load_id()
        self.load_last_login()

    def load_item_data(self):
        with open(self.items_loc, 'r') as item:
            self.items_data = load(item)

    def load_id(self):
        with open(self.id_loc, 'r') as item:
            self.id = load(item)

    def load_last_login(self):
        with open(self.last_login_loc, 'r') as item:
            self.last_login = load(item)

    def save_items_data(self, loc, items_data):
        with open(loc, 'w') as item:
            dump(items_data, item, indent=2)
