import yt_dlp
import os
import json
from pydub import AudioSegment
from utils.utils import get_time_milliseconds
from typing import Dict, List
from random import randint
from enum import Enum

class Controller:
    @staticmethod
    class State(Enum):
            IDLE = 0
            REQUEST = 1
            DOWNLOADING = 2
            POSTPROCESSING = 3
            DONE = 4
            ERROR = 5

    def __init__(self) -> None:
        self.ydl_opts: Dict[any] = {
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{  
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'noplaylist': True,
            'progress_hooks': [self.__progress_hook]
        }
        self.url: str = ''
        self.default_save_dir: str = f'{os.getcwd()}/downloads/'
        self.save_dir: str = ''
        self.custom_filename: str = ''
        self.save_filename: str = ''
        self.trim_filepath: str = ''
        self.trim_timestamps: Dict[List[int | float]] = {'start': [0, 0, 0], 'end': [0, 0, 0]}
        self.download_status: Dict[any] = {'progress': '', 'eta': '', 'speed': '', 
                                            'file_size': '', 'elapsed_time': ''}
        self.state: int = Controller.State.IDLE
        self.error_message: str = ''

        # Loads config from file
        self.load_config()

    @property
    def save_path(self) -> str:
        return os.path.join(self.save_dir, self.save_filename)
    
    def download(self) -> None:
        if self.url == '':
            self.error_message = 'No URL provided! >:('
            self.state = Controller.State.ERROR
            return
        
        self.state = Controller.State.REQUEST
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            if self.save_dir == '':
                os.makedirs('downloads', exist_ok=True)
                self.save_dir = self.default_save_dir

            if self.custom_filename == '':
                self.save_filename = f'%(title)s_{randint(0, 1000)}'
            else:
                self.save_filename = self.custom_filename
        
            self.ydl_opts['outtmpl']['default'] = self.save_path

            ydl.download([self.url])
            if self.should_trim:
                self.trim_audio_file(self.save_path)
            self.state = Controller.State.DONE
    
    @property
    def should_trim(self) -> bool:
        return self.trim_timestamps['start'] != [0, 0, 0] and self.trim_timestamps['end'] != [0, 0, 0]

    def trim_audio_file(self, filepath: str) -> None:
        time_start = get_time_milliseconds(self.trim_timestamps['start'])
        time_end = get_time_milliseconds(self.trim_timestamps['end'])

        audio = AudioSegment.from_mp3(filepath)
        audio = audio[time_start:] if time_end == 0 else audio[time_start:time_end]

        directory, file = os.path.split(filepath)
        file_no_extension, extention = os.path.splitext(file)
        filepath = os.path.join(directory, file_no_extension + '_trimmed' + extention)

        self.trim_filepath = filepath
        audio.export(filepath, format="mp3"), print(f"[TrimAudio] Audio trimmed and saved at {filepath}")
    
    def __progress_hook(self, d):
        if d['status'] == 'downloading':
            self.state = self.State.DOWNLOADING
            self.download_status['progress'] = d['_percent_str']
            self.download_status['eta'] = d['_eta_str']
            self.download_status['speed'] = d['_speed_str']
        if d['status'] == 'finished':
            self.state = self.State.POSTPROCESSING
            self.save_filename = os.path.split(d['filename'])[1] + '.mp3' # Adding extension to filename variable (yt_dlp adds by default to saved file)
            self.download_status['file_size'] = d['total_bytes']
            self.download_status['elapsed_time'] = d['elapsed']
        if d['status'] == 'error':
            self.state = self.State.ERROR
            self.error_message = d['error']
        
    def save_config(self) -> None:
        config = {
            'default_save_dir': self.default_save_dir,
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
    
    def load_config(self) -> None:
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.default_save_dir = config['default_save_dir']
        except FileNotFoundError:
            self.save_config()
            self.load_config()
    
    def set_default_save_dir(self, path: str) -> None:
        self.default_save_dir = path
        self.save_config()
    
    
