from controller.controller import Controller
from view.view import View

def main():
    controller = Controller()
    controller.trim_timestamps["start"] = [0, 0, 16]
    controller.trim_timestamps["end"] = [0, 0, 20]
    # controller.download()
    # controller.trim_audio_file(controller.save_path)

    window = View(controller)
    window.mainloop()

if __name__ == '__main__':
    main()