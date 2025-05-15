from PyQt6 import QtWidgets
from main_frame_class import MainFrame  # Import the main GUI frame from the new file

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec())