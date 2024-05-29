from controller.controller import Controller

def main():
    controller = Controller()
    url = 'https://www.youtube.com/watch?v=7ta7Nra289g'
    controller.url = url
    controller.download()
    controller.trim_timestamps["start"] = [0, 0, 0]
    controller.trim_timestamps["end"] = [0, 0, 1]
    controller.trim_audio_file(controller.save_path)

if __name__ == '__main__':
    main()