import customtkinter as ctk

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class View(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        # App interface

        self.title("MP3 YouTube Downloader")
        self.geometry(f"{1100}x{580}")

        # Title
        self.title_label = ctk.CTkLabel(self, text="MP3 YouTube Downloader", font=("Fira Sans", 20, 'bold'))
        self.title_label.pack(pady=10)

        # Path saved files
        self.path_label = ctk.CTkLabel(self, text="Path of saved files", font=("Fira Sans", 12))
        self.path_label.pack(padx=10, anchor='w')

        self.path_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.path_frame.pack(pady=5, padx=10, fill="x")

        print(self.controller.save_path)
        self.path_entry = ctk.CTkEntry(self.path_frame, width=400, placeholder_text=self.controller.default_save_dir)
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.path_entry.configure(state='disabled')

        # Path edit button
        self.select_button = ctk.CTkButton(self.path_frame, text="Edit", command=self.select_directory)
        self.select_button.pack(side="right", padx=5)

        # Download and trim buttons
        self.button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.button_frame.pack(pady=10)

        self.download_button = ctk.CTkButton(self.button_frame, text="Download", command=self.download)
        self.download_button.pack(side="left", padx=20)

        self.trim_button = ctk.CTkButton(self.button_frame, text="Trim", command=self.trim)
        self.trim_button.pack(side="right", padx=20)

    def select_directory(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, path)
            self.path_entry.configure(state="disabled")
    
    def download(self):
        print("download")

    def trim(self):
        print("trim")
    
    def button_function(self):
        print("button pressed")