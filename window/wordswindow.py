import os

from PySide2.QtWidgets import (QAbstractItemView, QDataWidgetMapper, QFileDialog,
                               QHeaderView, QMainWindow, QMessageBox)
from PySide2.QtGui import QKeySequence, QColor
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

from copy import deepcopy
import settings


class WordsListModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if self.mylist:
            return len(self.mylist[0])
        return 0

    def data(self, index, role):
        if not self.mylist:
            return None
        if not index.isValid():
            return None
        elif role == QtCore.Qt.DisplayRole:
            return self.mylist[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            if index.column() == 0 and global_data.behavior_data:
                statu = global_data.behavior_data[index.row()]
                color = Qt.white
                if statu == 1:
                    color = Qt.green
                elif statu == 2:
                    color = Qt.gray
                return QColor(color)
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        if not self.mylist:
            return
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
                _, filename = os.path.split(inFile.fileName())
                self.le_title.setText(str(filename))

    @Slot()
    def CreateWords(self):
        origin_words = Views().extract_english_words(self.txtPost.toPlainText())
        if not origin_words:
            self.init_data()
            self.tvWords.setModel(WordsListModel(
                self, [], global_data.word_list_header))
            return
        stop_words = DbInterface().get_stop_words()
        clean_words = Views().exclude_stop_words(origin_words, stop_words)
        clean_words = Views().filter_done_words(clean_words)
        if not clean_words:
            return
        word_type_dict = Views().get_word_type_dict(clean_words)
        star_words_dict = DbInterface().get_words_detail(clean_words)
        global_data.word_list_data = []
        global_data.behavior_data = []
        for word in clean_words:
            row = [str(word), '', '', '', '']
            detail = star_words_dict.get(str(word).lower(), {})
            if detail:
                row[1] = detail['translation']
                row[2] = detail['phonetic']
                row[3] = detail['definition']
                row[4] = word_type_dict.get(str(word), '')
            global_data.word_list_data.append(row)

            # 0:未读 1：已读  2：停用
            behavior_statu = 0
            if not detail:
                behavior_statu = 2
            global_data.behavior_data.append(behavior_statu)

        word_list = deepcopy(global_data.word_list_data)
        for word in word_list:
            word[4] = settings.NLTK_WORD_TYPE_DICT.get(word[4], '')

        self.tvWords.setModel(WordsListModel(
            self, word_list, global_data.word_list_header))

        global_data.post_data = {
            "title": self.le_title.text(),
            "url": self.le_url.text()
        }

        self.tvWords.setWordWrap(True)
        self.tvWords.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tvWords.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabWidget.setCurrentIndex(1)

    def tvWords_left_click(self, item):
        if item.column() == 0 and item.row() >= 0:
            statu = global_data.behavior_data[item.row()]
            global_data.behavior_data[item.row()] = (statu + 1) % 3

    @Slot()
    def tvWords_save(self):
        Views().save_word_list(
            global_data.word_list_data,
            global_data.behavior_data,
            global_data.post_data
        )

    def load_posts(self):
        self.tlwPost.clear()
        global_data.post_list = DbInterface().get_posts()
        post_list = [str(row['id']) + ":" + str(row['title'])
                     for row in global_data.post_list]
        self.tlwPost.addItems(post_list)

    @Slot()
    def tab_changed(self, index):
        if index == 0:
            self.load_posts()

    @Slot()
    def selected_post(self, item):
        post_id = int(str(item.data()).split(":")[0])
        if post_id:
            global_data.selected_post_id = post_id
            post_data = DbInterface().get_post(post_id)
            global_data.post_word_data = DbInterface().get_post_word_data(post_id)
            if not post_data:
                return
            self.le_title.setText(post_data['title'])
            self.le_url.setText(post_data['url'])
            self.txtPost.setPlainText(
                "\n".join([row['word'] for row in global_data.post_word_data]))

    def delete_post_node(self):
        if not global_data.selected_post_id:
            return
        Views().delete_post_words(global_data.selected_post_id)
        global_data.selected_post_id = 0
        self.load_posts()

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.btnLoad.clicked.connect(self.LoadFile)
        self.btnCreate.clicked.connect(self.CreateWords)
        # 鼠标左键点击事件
        self.tvWords.clicked.connect(self.tvWords_left_click)

        self.btn_words_save.clicked.connect(self.tvWords_save)

        self.tabWidget.currentChanged['int'].connect(self.tab_changed)
        self.tlwPost.clicked.connect(self.selected_post)

        self.btn_post_delete.clicked.connect(self.delete_post_node)

        self.load_posts()

    def init_data(self):
        global_data.word_list_data = []
        global_data.behavior_data = []
        global_data.post_data = {}
        global_data.post_list = []
        global_data.post_word_data = []
        global_data.selected_post_id = 0
