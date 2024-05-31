from controller.controller import Controller
from view.view import View

def main():
    controller = Controller()
    url = 'https://www.youtube.com/watch?v=7ta7Nra289g'
    controller.url = url
    controller.trim_timestamps["start"] = [0, 0, 16]
    controller.trim_timestamps["end"] = [0, 0, 20]
    # controller.download()
    # controller.trim_audio_file(controller.save_path)

    window = View(controller)
    window.mainloop()

if __name__ == '__main__':
    main()