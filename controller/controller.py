import yt_dlp
import os
from pydub import AudioSegment
from utils.utils import get_time_milliseconds, get_latest_file
from typing import Dict, List
from random import randint

class Controller:
    def __init__(self) -> None:
        self.ydl_opts: Dict[any] = {
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
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
        self.save_filename: str = ''
        self.trim_timestamps: Dict[List[int]] = {'start': [0, 0, 0], 'end': [0, 0, 0]}
        self.video_title: str = ''

    @property
    def save_path(self) -> str:
        return os.path.join(self.save_dir, self.save_filename)
    
    def download(self) -> None:
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            if self.save_dir == '':
                os.makedirs('downloads', exist_ok=True)
                self.save_dir = self.default_save_dir

            if self.save_filename == '':
                self.save_filename = f'%(title)s_{randint(0, 1000)}'  
        
            self.ydl_opts['outtmpl']['default'] = self.save_path

            ydl.download([self.url])

    def trim_audio_file(self, filepath: str) -> None:
        time_start = get_time_milliseconds(self.trim_timestamps['start'])
        time_end = get_time_milliseconds(self.trim_timestamps['end'])

        # Sketchy code to get full name of file (when downloading mp3, the extension is added 
        # by default, so it is not on the filename variable)
        filepath = filepath + '.mp3' if filepath[-3:] != 'mp3' else filepath

        audio = AudioSegment.from_mp3(filepath)
        audio = audio[time_start:] if time_end == 0 else audio[time_start:time_end]

        directory, file = os.path.split(filepath)
        file_no_extension, extention = os.path.splitext(file)
        filepath = os.path.join(directory, file_no_extension + '_trimmed' + extention)
        
        audio.export(filepath, format="mp3")
    
    def __progress_hook(self, d):
        if d['status'] == 'downloading':
            self.video_title = d.get('info_dict', {}).get('title', 'Unknown title')
            self.save_filename = self.save_filename.replace('%(title)s', self.video_title)
