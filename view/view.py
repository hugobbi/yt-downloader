import threading
import customtkinter as ctk
import re

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class View(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.update_time = 1
        self.initialize_interface()

    def initialize_interface(self):
        # App interface

        self.title("MP3 YouTube Downloader")
        self.geometry(f"{1200}x{480}")

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
        self.progress_bar.set(0)

        self.progress_percentage = ctk.CTkLabel(self.progress_frame, text="0%", font=("Fira Sans", 12))
        self.progress_percentage.pack(side="left", padx=10)

        # Log
        self.progress_log_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.progress_log_frame.pack(pady=10, fill="x")

        self.progress_log = ctk.CTkLabel(self.progress_log_frame, text="", font=("Fira Sans", 12))
        self.progress_log.pack(side="left", fill="y", expand=True)

        # Audio file settings window

        # Trim window

        # Updating values
        self.update_progress_bar()
        self.update_logs()


    def select_directory(self):
        path = ctk.filedialog.askdirectory(mustexist=True, title="Select directory to save files")
        if path:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, path)
            self.controller.save_dir = path
            self.path_entry.configure(state="disabled")
    
    def download(self):
        if not self.controller.state == self.controller.State.DOWNLOADING:
            self.controller.url = self.url_entry.get()
            download_thread = threading.Thread(target=self.controller.download)
            download_thread.start()

    def trim(self):
        print("trim")
    
    def file_settings(self):
        print("file settings")
    
    def update_progress_bar(self):
        # if self.controller.state == self.controller.State.IDLE:
        #     self.progress_label.grid_remove()
        #     self.progress_percentage.grid_remove()
        #     self.progress_bar.grid_remove()
        # else:
        #     self.progress_label.grid()
        #     self.progress_percentage.grid()
        #     self.progress_bar.grid()

        if self.controller.state == self.controller.State.DOWNLOADING:
            progress_str = self.__remove_ansi_escape_sequences(self.controller.download_status['progress'])
            self.progress_percentage.configure(text=f"{progress_str}")
            progress = float(progress_str.replace('%', ''))
            self.progress_bar.set(progress / 100)

        if self.controller.state == self.controller.State.POSTPROCESSING:
            self.progress_percentage.configure(text="100%")
            self.progress_bar.set(1)
        
        # Update progress bar every n milliseconds
        self.after(self.update_time, self.update_progress_bar)
    
    def update_logs(self):
        if self.controller.state == self.controller.State.IDLE:
            self.progress_log.configure(text="")
        if self.controller.state == self.controller.State.REQUEST:
            self.progress_log.configure(text="Requesting information...")
        if self.controller.state == self.controller.State.DOWNLOADING:
            self.progress_log.configure(text=f"Downloading... SPEED {self.controller.download_status['speed']} ETA {self.controller.download_status['eta']}")
        if self.controller.state == self.controller.State.POSTPROCESSING:
            self.progress_log.configure(text="Postprocessing...")
        if self.controller.state == self.controller.State.DONE:
            trim_info = "" if not self.controller.should_trim else f", {self.controller.trim_filepath}"
            self.progress_log.configure(text=f"Done! File saved at {self.controller.save_path}{trim_info}")
        if self.controller.state == self.controller.State.ERROR:
            self.progress_log.configure(text=f"An error occured: {self.controller.error_message}")
        
        # Update logs every n milliseconds
        self.after(self.update_time, self.update_logs)
    
    def __remove_ansi_escape_sequences(self, s):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', s)
        