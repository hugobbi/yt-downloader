from setuptools import setup, find_packages

setup(
    name='MP3 YouTube Downloader',
    author='Henrique Uhlmann Gobbi',
    author_email='hgugobbi@gmail.com',
    version=0.1,
    packages=find_packages(),
    install_requires=[
        'yt_dlp',
        'pydub'
    ],
    url='https://github.com/hugobbi/yt-downloader',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description='GUI Program to download and trim audio from YouTube videos.'
)