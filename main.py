from controller.controller import Controller
from view.view import View

def main():
    controller = Controller()
    window = View(controller)
    window.mainloop()

if __name__ == '__main__':
    main()