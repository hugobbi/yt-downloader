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

        # URL
        self.url_label = ctk.CTkLabel(self, text="YouTube URL", font=("Fira Sans", 12))
        self.url_label.pack(padx=10, anchor='w')

        self.url_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.url_frame.pack(pady=5, padx=10, fill="x")

        self.url_entry = ctk.CTkEntry(self.url_frame, width=400, placeholder_text='Insert URL here')
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_entry.bind("<KeyRelease>", self.update_url)

        # Path saved files
        self.path_label = ctk.CTkLabel(self, text="Path of saved files", font=("Fira Sans", 12))
        self.path_label.pack(padx=10, anchor='w')

        self.path_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.path_frame.pack(pady=5, padx=10, fill="x")

        self.path_entry = ctk.CTkEntry(self.path_frame, width=400, placeholder_text=self.controller.default_save_dir)
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.path_entry.configure(state='disabled')

        # Path edit button
        self.select_button = ctk.CTkButton(self.path_frame, text="Edit", command=self.select_directory)
        self.select_button.pack(side="right", padx=5)

        # Settings buttons
        self.settings_button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.settings_button_frame.pack(pady=10)

        self.file_settings_button = ctk.CTkButton(self.settings_button_frame, text="Audio file settings", command=self.file_settings)
        self.file_settings_button.pack(side="left")

        # Download and trim buttons
        self.action_button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.action_button_frame.pack(pady=10)

        self.download_button = ctk.CTkButton(self.action_button_frame, text="Download", height=50, command=self.download)
        self.download_button.pack(side="left")

        self.trim_button = ctk.CTkButton(self.action_button_frame, text="Trim", height=50, command=self.trim)
        self.trim_button.pack(side="right", padx=20)

        # Download progress
        self.progress_label = ctk.CTkLabel(self, text="Download progress", font=("Fira Sans", 12))
        self.progress_label.pack(padx=10, anchor='w')

        self.progress_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.progress_frame.pack(pady=10, fill="x")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=1000, height=20)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=10)

        self.progress_percentage = ctk.CTkLabel(self.progress_frame, text="", font=("Fira Sans", 12))
        self.progress_percentage.pack(side="left", padx=10)
        self.update_progress_percentage() # temporary

        # Log
        self.progress_log_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.progress_log_frame.pack(pady=10, fill="x")

        self.progress_log = ctk.CTkTextbox(self.progress_log_frame, width=100, height=10)
        self.progress_log.pack(side="left", fill="y", expand=True)

        # Audio file settings window

        # Trim window
        

    def select_directory(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, path)
            self.path_entry.configure(state="disabled")
    
    def update_url(self, event):
        self.controller.url = self.url_entry.get()
        print(self.controller.url)
    
    def download(self):
        print("download")

    def trim(self):
        print("trim")
    
    def file_settings(self):
        print("file settings")
    
    def update_progress_percentage(self):
        self.progress_percentage.configure(text=f"{0}%")