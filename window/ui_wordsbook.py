# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wordsbook.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1050, 899)
        self.space_click = QAction(MainWindow)
        self.space_click.setObjectName(u"space_click")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_op = QWidget()
        self.tab_op.setObjectName(u"tab_op")
        self.verticalLayout_8 = QVBoxLayout(self.tab_op)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tlwPost = QListWidget(self.tab_op)
        self.tlwPost.setObjectName(u"tlwPost")

        self.verticalLayout.addWidget(self.tlwPost)

        self.btn_post_delete = QPushButton(self.tab_op)
        self.btn_post_delete.setObjectName(u"btn_post_delete")

        self.verticalLayout.addWidget(self.btn_post_delete)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_2 = QGroupBox(self.tab_op)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.le_title = QLineEdit(self.groupBox_2)
        self.le_title.setObjectName(u"le_title")

        self.horizontalLayout_3.addWidget(self.le_title)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.le_url = QLineEdit(self.groupBox_2)
        self.le_url.setObjectName(u"le_url")

        self.horizontalLayout_4.addWidget(self.le_url)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.txtPost = QTextEdit(self.tab_op)
        self.txtPost.setObjectName(u"txtPost")

        self.verticalLayout_6.addWidget(self.txtPost)


        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)

        self.verticalLayout_8.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(self.tab_op)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnLoad = QPushButton(self.groupBox)
        self.btnLoad.setObjectName(u"btnLoad")

        self.horizontalLayout_2.addWidget(self.btnLoad)

        self.btnCreate = QPushButton(self.groupBox)
        self.btnCreate.setObjectName(u"btnCreate")

        self.horizontalLayout_2.addWidget(self.btnCreate)


        self.verticalLayout_8.addWidget(self.groupBox)

        self.tabWidget.addTab(self.tab_op, "")
        self.tab_words = QWidget()
        self.tab_words.setObjectName(u"tab_words")
        self.verticalLayout_3 = QVBoxLayout(self.tab_words)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")

        self.verticalLayout_3.addLayout(self.layout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cb_filter_words = QComboBox(self.tab_words)
        self.cb_filter_words.addItem("")
        self.cb_filter_words.addItem("")
        self.cb_filter_words.addItem("")
        self.cb_filter_words.addItem("")
        self.cb_filter_words.addItem("")
        self.cb_filter_words.addItem("")
        self.cb_filter_words.setObjectName(u"cb_filter_words")

        self.horizontalLayout_5.addWidget(self.cb_filter_words)

        self.btn_words_stop = QPushButton(self.tab_words)
        self.btn_words_stop.setObjectName(u"btn_words_stop")

        self.horizontalLayout_5.addWidget(self.btn_words_stop)

        self.btn_words_ouput = QPushButton(self.tab_words)
        self.btn_words_ouput.setObjectName(u"btn_words_ouput")

        self.horizontalLayout_5.addWidget(self.btn_words_ouput)

        self.horizontalLayout_5.setStretch(0, 100)
        self.horizontalLayout_5.setStretch(2, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.tvWords = QTableView(self.tab_words)
        self.tvWords.setObjectName(u"tvWords")
        self.tvWords.setDragEnabled(True)
        self.tvWords.setDragDropOverwriteMode(False)
        self.tvWords.setDragDropMode(QAbstractItemView.DragDrop)
        self.tvWords.setDefaultDropAction(Qt.MoveAction)
        self.tvWords.setSortingEnabled(True)

        self.verticalLayout_3.addWidget(self.tvWords)

        self.btn_words_save = QPushButton(self.tab_words)
        self.btn_words_save.setObjectName(u"btn_words_save")

        self.verticalLayout_3.addWidget(self.btn_words_save)

        self.tabWidget.addTab(self.tab_words, "")
        self.tab_phrase = QWidget()
        self.tab_phrase.setObjectName(u"tab_phrase")
        self.verticalLayout_4 = QVBoxLayout(self.tab_phrase)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.cbPhrase = QComboBox(self.tab_phrase)
        self.cbPhrase.setObjectName(u"cbPhrase")

        self.verticalLayout_4.addWidget(self.cbPhrase)

        self.tvPhrase = QTableView(self.tab_phrase)
        self.tvPhrase.setObjectName(u"tvPhrase")

        self.verticalLayout_4.addWidget(self.tvPhrase)

        self.tabWidget.addTab(self.tab_phrase, "")

        self.verticalLayout_7.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.space_click.setText(QCoreApplication.translate("MainWindow", u"space_click", None))
#if QT_CONFIG(shortcut)
        self.space_click.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))
#endif // QT_CONFIG(shortcut)
        self.btn_post_delete.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8be6\u7ec6\u4fe1\u606f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6807\u9898:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"URL: ", None))
        self.txtPost.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c", None))
        self.btnLoad.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6", None))
        self.btnCreate.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u5355\u8bcd\u672c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_op), QCoreApplication.translate("MainWindow", u"\u6587\u7ae0\u64cd\u4f5c", None))
        self.cb_filter_words.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5168\u90e8", None))
        self.cb_filter_words.setItemText(1, QCoreApplication.translate("MainWindow", u"\u672a\u8bfb", None))
        self.cb_filter_words.setItemText(2, QCoreApplication.translate("MainWindow", u"\u6807\u8bb0", None))
        self.cb_filter_words.setItemText(3, QCoreApplication.translate("MainWindow", u"\u638c\u63e1", None))
        self.cb_filter_words.setItemText(4, QCoreApplication.translate("MainWindow", u"\u505c\u7528", None))
        self.cb_filter_words.setItemText(5, QCoreApplication.translate("MainWindow", u"\u975e\u505c\u7528", None))

        self.btn_words_stop.setText(QCoreApplication.translate("MainWindow", u"+1", None))
        self.btn_words_ouput.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u5355\u8bcd", None))
        self.btn_words_save.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u72b6\u6001", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_words), QCoreApplication.translate("MainWindow", u"\u5355\u8bcd\u672c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_phrase), QCoreApplication.translate("MainWindow", u"\u77ed\u8bed\u672c", None))
    # retranslateUi

