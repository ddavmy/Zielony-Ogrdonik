import asyncio
import threading
from multiprocessing import Event, Queue

import customtkinter as ctk

gui_ready_event = Event()
login_data_queue = Queue()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

appWidth, appHeight = 400, 400

def signal_ready():
    gui_ready_event.set()

class LoginGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.login_button = None
        self.username_entry = None
        self.password_entry = None
        self.server_option = None
        self.server_label = None
        self.label = None
        self.title("Logowanie")
        self.geometry(f"{appWidth}x{appHeight}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self, corner_radius=10)
        self.login_frame.grid(row=0, column=0, padx=40, pady=40)
        self.create_login_frame()

    def create_login_frame(self):
        self.label = ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 20))
        self.label.pack(pady=20)

        self.server_label = ctk.CTkLabel(self.login_frame, text="Wybierz Serwer")
        self.server_label.pack(pady=10)

        self.server_option = ctk.CTkOptionMenu(self.login_frame, values=[str(i) for i in range(1, 22)])
        self.server_option.pack(pady=10, padx=20)

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Nazwa")
        self.username_entry.pack(pady=10, padx=20)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Hasło", show="*")
        self.password_entry.pack(pady=10, padx=20)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login_to_site_wrapper)
        self.login_button.pack(pady=20)

    def login_to_site_wrapper(self):
        threading.Thread(target=self.run_async_login, daemon=True).start()

    async def login_to_site(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        server = "server" + self.server_option.get()
        login_data_queue.put((username, password, server))
        self.after(100, signal_ready)

    def run_async_login(self):
        asyncio.run(self.login_to_site())
