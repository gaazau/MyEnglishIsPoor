from __future__ import print_function, absolute_import

from PySide2.QtWidgets import (QAbstractItemView, QDataWidgetMapper,QFileDialog,
    QHeaderView, QMainWindow, QMessageBox)
from PySide2.QtGui import QKeySequence
from PySide2.QtSql import QSqlRelation, QSqlRelationalTableModel, QSqlTableModel
from PySide2.QtCore import Qt, Slot, QFile
# import createdb
from ui_wordsbook import Ui_MainWindow
# from bookdelegate import BookDelegate

from PySide2.QtSql import QSqlRelation, QSqlRelationalTableModel, QSqlTableModel

from core.views import Views


import operator
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


class WordsListModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
                                key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))

class WordsWindow(QMainWindow, Ui_MainWindow):
    """A window to show the books available"""

    @Slot()
    def LoadFile(self):
        path = QFileDialog.getOpenFileName(self, "Open File",
            '', "Any Files (*.*)")

        if path:
            inFile = QFile(path[0])
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = inFile.readAll()
                text = str(text, encoding='utf8')
                self.txtPost.setPlainText(text)

    @Slot()
    def CreateWords(self):
        origin_words = Views().extract_english_words(self.txtPost.toPlainText())
        stop_words = []
        clean_words = Views().exclude_stop_words(origin_words, stop_words)
        if not clean_words:
            return
        data_list = []
        header = ['单词', '英文定义', '中文定义', '发音', '词性分类']
        for word in clean_words:
            row = ['', '', '', '', '']
            row[0] = str(word)
            data_list.append(row)
        
        self.tvWords.setModel(WordsListModel(self, data_list, header))
        # set column width to fit contents (set font first!)
        self.tvWords.resizeColumnsToContents()
        self.tabWidget.setCurrentIndex(1)


    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.btnLoad.clicked.connect(self.LoadFile)
        self.btnCreate.clicked.connect(self.CreateWords)