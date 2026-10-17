
import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class EONWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EON — Personal AI Agent")
        self.resize(1000, 650)

        welcome = QLabel(
            "EON\n\nYour personal AI companion starts here."
        )
        welcome.setStyleSheet(
            """
            QLabel {
                color: #e5e7eb;
                background-color: #111827;
                font-size: 24px;
                padding: 40px;
            }
            """
        )
        welcome.setWordWrap(True)
        self.setCentralWidget(welcome)

        self.setStyleSheet("QMainWindow { background-color: #111827; }")


def main():
    app = QApplication(sys.argv)
    window = EONWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
