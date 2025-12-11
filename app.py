import os
from controller import AppController
from views import MainWindow

def main():
    # Enable ANSI colors in Windows CMD if needed (simple hack) - Not needed for GUI but good practice
    os.system('') 

    controller = AppController()
    app = MainWindow(controller)
    app.mainloop()

if __name__ == "__main__":
    main()
