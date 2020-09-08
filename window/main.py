import sys
from PySide2.QtWidgets import QApplication
from wordswindow import WordsWindow

if __name__ == "__main__":
    app = QApplication([])

    window = WordsWindow()
    window.resize(600, 800)
    window.show()

    sys.exit(app.exec_())
