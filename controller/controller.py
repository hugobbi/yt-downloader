import yt_dlp
import os
from pydub import AudioSegment
from utils.utils import get_time_milliseconds
from typing import Dict, List
from random import randint
from enum import Enum

class Controller:
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
        self.trim_timestamps: Dict[List[int | float]] = {'start': [0, 0, 0], 'end': [0, 0, 0]}
        self.download_status: Dict[any] = {'progress': '', 'eta': '', 'speed': '', 
                                            'file_size': '', 'elapsed_time': ''}
        self.is_downloading: bool = False
        self.state: int = self.State.IDLE

        class State(Enum):
            IDLE = 0
            REQUEST = 1
            DOWNLOADING = 2
            EXTRACTING = 3
            TRIMMING = 4
            DONE = 5

    @property
    def save_path(self) -> str:
        return os.path.join(self.save_dir, self.save_filename)
    
    def download(self) -> None:
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            if self.save_dir == '':
                os.makedirs('downloads', exist_ok=True)
                self.save_dir = self.default_save_dir

            if self.custom_filename == '':
                self.save_filename = f'%(title)s_{randint(0, 1000)}'  
        
            self.ydl_opts['outtmpl']['default'] = self.save_path

            ydl.download([self.url])

    def trim_audio_file(self, filepath: str) -> None:
        time_start = get_time_milliseconds(self.trim_timestamps['start'])
        time_end = get_time_milliseconds(self.trim_timestamps['end'])

        audio = AudioSegment.from_mp3(filepath)
        audio = audio[time_start:] if time_end == 0 else audio[time_start:time_end]

        directory, file = os.path.split(filepath)
        file_no_extension, extention = os.path.splitext(file)
        filepath = os.path.join(directory, file_no_extension + '_trimmed' + extention)

        audio.export(filepath, format="mp3"), print(f"[TrimAudio] Audio trimmed and saved at {filepath}")
    
    def __progress_hook(self, d):
        if d['status'] == 'downloading':
            self.download_status['progress'] = d['_percent_str']
            self.download_status['eta'] = d['_eta_str']
            self.download_status['speed'] = d['_speed_str']
            self.is_downloading = True
            self.state = self.State.DOWNLOADING
        if d['status'] == 'finished':
            self.save_filename = os.path.split(d['filename'])[1] + '.mp3' # Adding extension to filename variable (yt_dlp adds by default to saved file)
            self.download_status['file_size'] = d['total_bytes']
            self.download_status['elapsed_time'] = d['elapsed']
            self.is_downloading = False
            self.state = self.State.DONE
