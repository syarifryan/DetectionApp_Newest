# import sys
# import os
# from PyQt5.QtWidgets import QApplication
# from gui.main_window import MainWindow

# def main():
#     app = QApplication(sys.argv)
#     w = MainWindow()
#     w.show()
#     sys.exit(app.exec_())
#     os.makedirs("temp", exist_ok=True)
#     os.makedirs("output", exist_ok=True)

# if __name__ == '__main__':
#     main()

# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    app = QApplication(sys.argv)

    # Load dan terapkan QSS theme
    with open("gui/style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
