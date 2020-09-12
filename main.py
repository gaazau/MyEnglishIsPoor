import sys
from PySide2.QtWidgets import QApplication
from gui.wordswindow import WordsWindow

if __name__ == "__main__":
    app = QApplication([])

    window = WordsWindow()
    window.show()

    sys.exit(app.exec_())
