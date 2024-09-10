import asyncio
import threading
from multiprocessing import Event, Queue
import customtkinter as ctk
from src.actions import click_div_with_selected_plant, search_plants

gui_ready_event = Event()
login_data_queue = Queue()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

appWidth, appHeight = 400, 400

def signal_ready():
    gui_ready_event.set()

class LoginGui(ctk.CTk):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.title("Zielony Ogrodnik")
        self.geometry(f"{appWidth}x{appHeight}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = LoginFrame(self, page)
        self.plant_selection_frame = PlantSelectionFrame(self, page)

        self.show_frame(self.login_frame)

    def show_frame(self, frame):
        frame.tkraise()

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, page):
        super().__init__(parent, page)
        self.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

        self.parent = parent

        self.label = ctk.CTkLabel(self, text="Login", font=("Arial", 20))
        self.label.pack(pady=20)

        self.server_label = ctk.CTkLabel(self, text="Wybierz Serwer")
        self.server_label.pack(pady=10)

        self.server_option = ctk.CTkOptionMenu(self, values=[str(i) for i in range(1, 22)])
        self.server_option.pack(pady=10, padx=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nazwa")
        self.username_entry.pack(pady=10, padx=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Hasło", show="*")
        self.password_entry.pack(pady=10, padx=20)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_to_site_wrapper)
        self.login_button.pack(pady=20)

    def login_to_site_wrapper(self):
        threading.Thread(target=self.run_async_login, daemon=True).start()

    async def login_to_site(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        server = "server" + self.server_option.get()
        login_data_queue.put((username, password, server))

        self.parent.show_frame(self.parent.plant_selection_frame)

    def run_async_login(self):
        asyncio.run(self.login_to_site())

class PlantSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, page):
        super().__init__(parent)
        self.page = page
        self.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

        self.parent = parent
        self.server_option = None
        self.product_code_lookup = {}
        self.selected_plant_code = None

        threading.Thread(target=self.load_plants_data(page), daemon=True).start()

    def load_plants_data(self, page):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        plant_data = loop.run_until_complete(search_plants())
        loop.close()

        product_names, product_code_lookup = plant_data

        self.create_plant_selection_frame(page, product_names, product_code_lookup)

    def create_plant_selection_frame(self, page, product_names, product_code_lookup):
        self.server_label = ctk.CTkLabel(self, text="Co chcesz posadzić?")
        self.server_label.pack(pady=10)

        self.server_option = ctk.CTkOptionMenu(self, values=product_names, command=self.on_option_select)
        self.server_option.pack(pady=10, padx=20)

        self.product_code_lookup = product_code_lookup

        self.submit_button = ctk.CTkButton(self, text="Zasiej", command=self.plant_selected_plant(page))
        self.submit_button.pack(pady=20)

        threading.Thread(target=self.maximize_browser_and_signal_ready, args=(page,), daemon=True).start()

    def maximize_browser_and_signal_ready(self):
        signal_ready()

    def on_option_select(self, selected_name):
        self.selected_plant_code = self.product_code_lookup.get(selected_name)
        print(f"Nazwa: {selected_name}, Kod: {self.selected_plant_code}")

    def plant_selected_plant(self, page):
        if self.selected_plant_code is not None:
            print("Kod: ", self.selected_plant_code)
            threading.Thread(target=self.run_planting(page), daemon=True).start()
        else:
            print("No plant selected.")

    def run_planting(self, page):
        signal_ready()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.plant_selected_plant_async(page))
        loop.close()

    async def plant_selected_plant_async(self, page):
        if self.selected_plant_code is not None:
            print('KOD: ', self.selected_plant_code)
            await click_div_with_selected_plant(self.selected_plant_code, page)
