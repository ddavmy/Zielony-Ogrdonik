import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

appWidth, appHeight = 300, 300

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Zielony Ogrodnik")
        self.geometry(f"{appWidth}x{appHeight}")

        self.plantLabel = ctk.CTkLabel(self,
                                       text="Sadzimy")
        self.plantLabel.grid(row=3, column=0,
                                  padx=20, pady=20,
                                  sticky="ew")

        self.plantOptionMenu = ctk.CTkOptionMenu(self,
                                                 values=["Sałata",
                                                         "Marchew"])
        self.plantOptionMenu.grid(row=3, column=1,
                                  padx=20, pady=20,
                                  columnspan=2, sticky="ew")

        self.waterPlantsLabel = ctk.CTkLabel(self,
                                             text="Podlewamy?")
        self.waterPlantsLabel.grid(row=4, column=0,
                                   padx=20, pady=20,
                                   sticky="ew")

        self.waterPlantsCheckboxVar = ctk.StringVar(value="True")

        self.waterPlantsCheckbox = ctk.CTkCheckBox(self, text="",
                                                   variable=self.waterPlantsCheckboxVar,
                                                   onvalue="True",
                                                   offvalue="False")
        self.waterPlantsCheckbox.grid(row=4, column=1, padx=20,
                                      pady=20, sticky="ew")

        self.plantButton = ctk.CTkButton(self,
                                         text="Zasiej")
        self.plantButton.grid(row=5, column=1,
                              columnspan=2,
                              padx=20, pady=20,
                              sticky="ew")

if __name__ == "__main__":
    app = App()
    app.mainloop()