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
from core.views import GlobalData

from copy import deepcopy
import settings


class WordsListModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, behavior_dict, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
        self.behavior_dict = behavior_dict

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
            if index.column() == 0 and self.behavior_dict:
                statu = self.behavior_dict[self.mylist[index.row()][index.column()]]
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
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # 注册事件
        self.btnLoad.clicked.connect(self.load_file)
        self.btnCreate.clicked.connect(self.create_word_list)
        self.tvWords.clicked.connect(self.tvWords_left_click)
        self.btn_words_save.clicked.connect(self.update_word_list)
        self.tabWidget.currentChanged['int'].connect(self.tab_changed)
        self.tlwPost.clicked.connect(self.selected_post)
        self.btn_post_delete.clicked.connect(self.delete_post_node)

        self.load_posts()

    def load_posts(self):
        """加载文章列表"""
        self.tlwPost.clear()
        posts = DbInterface().get_posts()
        post_list = [str(row['id']) + ":" + str(row['title'])
                     for row in posts]
        self.tlwPost.addItems(post_list)

    @Slot()
    def tab_changed(self, index):
        """tab页切换"""
        if index == 0:
            self.load_posts()

    @Slot()
    def selected_post(self, item):
        """选中文章节点"""
        post_id = int(str(item.data()).split(":")[0])
        if post_id:
            post_data = DbInterface().get_post(post_id)
            post_words = DbInterface().get_post_word_data(post_id)
            print(post_words)
            self.refresh_control_post(
                    post_id=post_id,
                    title=post_data['title'],
                    url=post_data['url'],
                    data="\n".join([row['word'] for row in post_words]),
            )
    @Slot()        
    def delete_post_node(self):
        """删除文章节点"""
        if not GlobalData.selected_post['post_id']:
            return
        Views().delete_post_words(GlobalData.selected_post['post_id'])
        self.refresh_control_post()
        self.load_posts()
        
    @Slot()
    def load_file(self):
        """加载外部文件获取文章"""
        path = QFileDialog.getOpenFileName(
            self, "Open File", '', "Any Files (*.*)")
        if path:
            inFile = QFile(path[0])
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = str(inFile.readAll(), encoding='utf8')
                self.txtPost.setPlainText(text)
                _, filename = os.path.split(inFile.fileName())
                self.le_title.setText(str(filename))
                self.refresh_control_post(
                    post_id=0,
                    title=filename,
                    url="",
                    data=text,
                )

    def refresh_control_post(self, post_id=0, title="", url="", data=""):
        """刷新文章控件内容"""
        self.le_title.setText(title)
        self.le_url.setText(url)
        self.txtPost.setText(data)
        GlobalData.set_selected_post(
                post_id=post_id,
                title=title,
                url=url,
            )
    @Slot()
    def create_word_list(self):
        """创建文章对应单词表，过滤得到所有未读单词"""
        post_id = DbInterface().create_or_update_post(
            post_id=GlobalData.selected_post['post_id'],
            title=self.le_title.text(),
            url=self.le_url.text()
        )
        words = GlobalData.create_post_words_full(self.txtPost.toPlainText())
        DbInterface().create_or_update_post_words(post_id, words)
        GlobalData.init_behavior_dict()
        self.refresh_control_post(
            post_id,
            self.le_title.text(), 
            self.le_url.text(), 
            "\n".join([word for word in words])
        )
        self.refresh_control_word_list(filter_mode="unread")
        self.tabWidget.setCurrentIndex(1)

    def refresh_control_word_list(self, filter_mode="unread"):
        """刷新单词表控件"""
        filter_words = self.filter_word_list(filter_mode)
        word_list_shown = GlobalData.get_word_list_shown(filter_words)
        model = WordsListModel(self, word_list_shown, GlobalData.word_list_header, GlobalData.behavior_dict)
        self.tvWords.setModel(model)
        self.tvWords.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tvWords.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def filter_word_list(self, filter_mode="all"):
        """单词过滤"""
        if filter_mode == "unread":
            filter_words = []
            for word in GlobalData.post_data['word_list']:
                if GlobalData.behavior_dict[word] == 0:
                    filter_words.append(word)
            return filter_words
        return deepcopy(GlobalData.post_data['word_list'])

    @Slot()
    def tvWords_left_click(self, item):
        """单词点击，修改单词已读未读状态"""
        if item.column() == 0 and item.row() >= 0:
            statu = GlobalData.behavior_dict[item.data()]
            GlobalData.behavior_dict[item.data()] = (statu + 1) % 3

    @Slot()
    def update_word_list(self):
        """更新单词表当前状态"""
        post_id = Views().update_word_list(
            # GlobalData.word,
            global_data.word_list_data,
            global_data.behavior_data,
            global_data.post_data
        )
        self.refresh_control_word_list(filter_mode="unread")
