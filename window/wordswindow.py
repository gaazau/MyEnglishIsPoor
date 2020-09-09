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

from db.db_interface import DbInterface
import global_data


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
        if not origin_words:
                return
        stop_words = DbInterface().get_stop_words()
        clean_words = Views().exclude_stop_words(origin_words, stop_words)
        if not clean_words:
            return
        star_words_dict = DbInterface().get_words_detail(clean_words)
        global_data.word_list_data = [] 
        header = ['单词', '中文定义', '发音', '英文定义', '词性分类']
        for word in clean_words:
            row = [str(word), '', '', '', '']
            detail = star_words_dict.get(str(word).lower(), {})
            if detail:
                row[1] = detail['translation']
                row[2] = detail['phonetic']
                row[3] = detail['definition']
            global_data.word_list_data.append(row)
        
        self.tvWords.setModel(WordsListModel(self, global_data.word_list_data, header))
        self.tvWords.setWordWrap(True)
        self.tvWords.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tvWords.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabWidget.setCurrentIndex(1)


    def tvWords_left_click(self, item):
        if item.column() == 0 and item.row()>=0:
            print(global_data.word_list_data[item.row()])

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.btnLoad.clicked.connect(self.LoadFile)
        self.btnCreate.clicked.connect(self.CreateWords)
        # 鼠标左键点击事件
        self.tvWords.clicked.connect(self.tvWords_left_click)