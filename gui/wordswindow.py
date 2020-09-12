import os
import operator
from datetime import datetime
from copy import deepcopy

from PySide2.QtWidgets import (QAbstractItemView, QDataWidgetMapper, QFileDialog,
                               QHeaderView, QMainWindow, QMessageBox)
from PySide2.QtGui import QKeySequence, QColor
from PySide2.QtSql import QSqlRelation, QSqlRelationalTableModel, QSqlTableModel
from PySide2.QtCore import Qt, Slot, QFile
from PySide2.QtSql import QSqlRelation, QSqlRelationalTableModel, QSqlTableModel
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import settings
from core.views import GlobalData
from core.upload import upload_to_bbdc
from core.views import Views
from core.db.db_interface import DbInterface
from gui.ui.ui_wordsbook import Ui_MainWindow


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
                statu = self.behavior_dict[self.mylist[index.row(
                )][index.column()]]
                color = Qt.white
                if statu == 1:
                    color = Qt.green
                elif statu == 2:
                    color = Qt.gray
                elif statu == 3:
                    color = Qt.red
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
        self.cb_filter_words.currentIndexChanged.connect(
            self.change_filter_mode)
        self.btn_words_stop.clicked.connect(self.stop_current_words)
        self.btn_words_ouput.clicked.connect(self.output_word_list)
        self.btn_upload_bbdc.clicked.connect(self.upload_to_bbdc)

        self.cb_filter_words.setCurrentIndex(1)
        GlobalData.reset_data()
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
            self.refresh_control_post(
                post_id=post_id,
                title=post_data['title'],
                url=post_data['url'],
                data="\n".join([row['word'] for row in post_words]),
            )
            words = GlobalData.get_post_words(self.txtPost.toPlainText())
            GlobalData.init_behavior_dict()
            self.refresh_control_word_list()

    @Slot()
    def delete_post_node(self):
        """删除文章节点"""
        if not GlobalData.selected_post['post_id']:
            return
        Views().delete_post_words(GlobalData.selected_post['post_id'])
        GlobalData.reset_data()
        self.refresh_control_post()
        self.refresh_control_word_list()
        self.load_posts()

    @Slot()
    def load_file(self):
        """加载外部文件获取文章"""
        path = QFileDialog.getOpenFileName(
            self, "Open File", '', "Any Files (*.*)")
        if path:
            try:
                inFile = QFile(path[0])
                if inFile.open(QFile.ReadOnly | QFile.Text):
                    text = str(inFile.readAll(), encoding='utf8')
                    _, filename = os.path.split(inFile.fileName())
                    self.refresh_control_post(
                        post_id=0,
                        title=filename,
                        url="",
                        data=text,
                    )
            except Exception as ex:
                self.statusBar().showMessage("文件读取错误:%s" % str(ex))

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
        """创建文章对应单词表,过滤得到所有未读单词"""
        post_id = DbInterface().create_post(
            title=self.le_title.text(),
            url=self.le_url.text()
        )
        words = GlobalData.get_post_words(self.txtPost.toPlainText())
        GlobalData.init_behavior_dict()

        DbInterface().save_word_list(GlobalData.word_list_to_db())
        DbInterface().create_or_update_post_words(post_id, words)
        DbInterface().save_behavior(GlobalData.behavior_list_to_db())

        self.refresh_control_post(
            post_id,
            self.le_title.text(),
            self.le_url.text(),
            "\n".join([word for word in words])
        )
        self.refresh_control_word_list()
        self.tabWidget.setCurrentIndex(1)

    def refresh_control_word_list(self):
        """刷新单词表控件"""
        filter_words = self.filter_word_list(GlobalData.words_filter_mode)
        GlobalData.current_words = deepcopy(filter_words)
        word_list_shown = GlobalData.get_word_list_shown(filter_words)
        model = WordsListModel(
            self, word_list_shown, GlobalData.word_list_header, GlobalData.behavior_dict)
        self.tvWords.setModel(model)
        self.tvWords.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tvWords.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.statusBar().showMessage("共 %s 个单词" % len(word_list_shown))

    def filter_word_list(self, filter_mode=0):
        """单词过滤

        0:全部 1:未读 2:标记 3:掌握 4:停用 5: 非停用
        """
        filter_mode_dict = {
            0: (0, 1, 2, 3),
            1: (0,),
            2: (1,),
            3: (2,),
            4: (3,),
            5: (0, 1, 2),
        }
        filter_words = []

        for word in GlobalData.post_data['word_list']:
            if GlobalData.behavior_dict[word] in filter_mode_dict.get(filter_mode, 0):
                filter_words.append(word)
        return filter_words

    @Slot()
    def tvWords_left_click(self, item):
        """单词点击,修改单词已读未读状态"""
        if item.column() == 0 and item.row() >= 0:
            statu = GlobalData.behavior_dict[item.data()]
            GlobalData.behavior_dict[item.data()] = (statu + 1) % 4

    @Slot()
    def update_word_list(self):
        """更新单词表当前状态"""
        word_list = GlobalData.word_list_to_db()
        behavior_list = GlobalData.behavior_list_to_db()
        Views().update_word_list(word_list, behavior_list)
        self.refresh_control_word_list()

    @Slot()
    def change_filter_mode(self, index):
        if not index:
            GlobalData.words_filter_mode = 0
        else:
            GlobalData.words_filter_mode = index
        self.refresh_control_word_list()

    @Slot()
    def stop_current_words(self):
        if not GlobalData.current_words:
            return
        counter_dict = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
        }
        for word in GlobalData.current_words:
            if word in GlobalData.behavior_dict:
                GlobalData.behavior_dict[word] = (
                    GlobalData.behavior_dict[word] + 1) % 4
                counter_dict[GlobalData.behavior_dict[word]] += 1
        show_words = "*当前单词状态:({}未读,{}标记,{}掌握,{}停用)".format(
            counter_dict[0],
            counter_dict[1],
            counter_dict[2],
            counter_dict[3],
        )
        tip_words = "共 %s 个单词" % len(GlobalData.current_words)
        self.statusBar().showMessage(tip_words + " " + show_words)

    @Slot()
    def output_word_list(self):
        filter_words = GlobalData.current_words
        if not filter_words:
            return
        words = "\n".join(sorted([str(word) for word in filter_words]))

        fname, ftype = QFileDialog.getSaveFileName(
            self, 'save file', './', "ALL (*.*)")
        with open(fname, 'w') as fn:
            fn.write(words)
        tip_words = "共 %s 个单词" % len(filter_words)
        tip_other = "已导出单词本:%s" % fname
        self.statusBar().showMessage(tip_words + " " + tip_other)

    @Slot()
    def upload_to_bbdc(self):
        filter_words = GlobalData.current_words
        if not filter_words:
            return
        flag = QMessageBox.question(
            self, "上传当前单词", "是否上传至不背单词?\n官网：%s" % "bbdc.cn")

        if str(flag)[-1] != 's':
            return
        tip_words = "共 %s 个单词" % len(filter_words)
        try:
            if not upload_to_bbdc.MY_COOKIES:
                upload_to_bbdc.login_bbdc()
            result = upload_to_bbdc.post_my_list(
                ",".join(filter_words),
                name=self.le_title.text()[:15],
                desc="%s:%s" % (settings.FILTER_MODE[GlobalData.words_filter_mode], datetime.now(
                ).strftime("%Y-%m-%d"))
            )
            msg = tip_words + " 上传成功-%s" % datetime.now().strftime("%H:%M:%S")
        except Exception as ex:
            msg = tip_words + \
                " 上传失败-%s:%s" % (datetime.now().strftime("%H:%M:%S"), str(ex))
        self.statusBar().showMessage(msg)
