import customtkinter as ctk

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class View(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MP3 YouTube Downloader")
        self.geometry(f"{1100}x{580}")

        self.button = ctk.CTkButton(master=self, text="Download", command=self.button_function)
        self.button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    def button_function(self):
        print("button pressed")
    