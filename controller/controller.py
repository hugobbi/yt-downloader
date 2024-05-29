import yt_dlp
import os
from pydub import AudioSegment
from utils.utils import get_current_time_string, get_time_milliseconds
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
        }

        self.url: str = ''
        self.default_save_path: str = f'{os.getcwd()}/downloads/'
        self.save_path: str = ''
        self.custom_filename: str = ''
        self.trim_timestamps: Dict[List[int]] = {'start': [0, 0, 0], 'end': [0, 0, 0]}
        self.should_trim: bool = False
    
    def download(self) -> None:
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            # if self.save_path == '':
            #     os.makedirs('downloads', exist_ok=True)
            #     self.save_path = self.default_save_path

            # filename = ''
            # if self.custom_filename == '':
            #     info_dict = ydl.extract_info(self.url, download=False)
            #     video_title = info_dict.get('title', 'video') + f'_{get_current_time_string()}'
            #     filename = video_title
            # else: 
            #     filename = self.custom_filename

            # self.save_path += filename 
            # self.ydl_opts['outtmpl']['default'] = self.save_path
            self.ydl_opts['outtmpl']['default'] = f'%(title)s_aaa{randint(0, 1000)}'
            ydl.download([self.url])
    
    def trim_audio_file(self, filepath: str) -> None:
        time_start = get_time_milliseconds(self.trim_timestamps['start'])
        time_end = get_time_milliseconds(self.trim_timestamps['end'])

        audio = AudioSegment.from_mp3(filepath)
        audio = audio[time_start:] if time_end == 0 else audio[time_start:time_end]
        
        audio.export(filepath + "_trimed", format="mp3")


        