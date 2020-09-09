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
        MainWindow.resize(906, 880)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_op = QWidget()
        self.tab_op.setObjectName(u"tab_op")
        self.verticalLayout_2 = QVBoxLayout(self.tab_op)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.txtPost = QTextEdit(self.tab_op)
        self.txtPost.setObjectName(u"txtPost")

        self.verticalLayout_2.addWidget(self.txtPost)

        self.groupBox = QGroupBox(self.tab_op)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnLoad = QPushButton(self.groupBox)
        self.btnLoad.setObjectName(u"btnLoad")

        self.horizontalLayout.addWidget(self.btnLoad)

        self.btnCreate = QPushButton(self.groupBox)
        self.btnCreate.setObjectName(u"btnCreate")

        self.horizontalLayout.addWidget(self.btnCreate)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.tabWidget.addTab(self.tab_op, "")
        self.tab_words = QWidget()
        self.tab_words.setObjectName(u"tab_words")
        self.verticalLayout_3 = QVBoxLayout(self.tab_words)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.btn_words_save = QPushButton(self.tab_words)
        self.btn_words_save.setObjectName(u"btn_words_save")

        self.layout.addWidget(self.btn_words_save)

        self.pushButton = QPushButton(self.tab_words)
        self.pushButton.setObjectName(u"pushButton")

        self.layout.addWidget(self.pushButton)


        self.verticalLayout_3.addLayout(self.layout)

        self.tvWords = QTableView(self.tab_words)
        self.tvWords.setObjectName(u"tvWords")
        self.tvWords.setSortingEnabled(True)

        self.verticalLayout_3.addWidget(self.tvWords)

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
        self.tab_grammer = QWidget()
        self.tab_grammer.setObjectName(u"tab_grammer")
        self.verticalLayout_5 = QVBoxLayout(self.tab_grammer)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.cbGrammer = QComboBox(self.tab_grammer)
        self.cbGrammer.setObjectName(u"cbGrammer")

        self.verticalLayout_5.addWidget(self.cbGrammer)

        self.tvGrammer = QTableView(self.tab_grammer)
        self.tvGrammer.setObjectName(u"tvGrammer")

        self.verticalLayout_5.addWidget(self.tvGrammer)

        self.tabWidget.addTab(self.tab_grammer, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.txtPost.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c", None))
        self.btnLoad.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u6587\u4ef6", None))
        self.btnCreate.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u5355\u8bcd\u672c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_op), QCoreApplication.translate("MainWindow", u"\u6587\u7ae0\u64cd\u4f5c", None))
        self.btn_words_save.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u72b6\u6001", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_words), QCoreApplication.translate("MainWindow", u"\u5355\u8bcd\u672c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_phrase), QCoreApplication.translate("MainWindow", u"\u77ed\u8bed\u672c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_grammer), QCoreApplication.translate("MainWindow", u"\u53e5\u578b\u672c", None))
    # retranslateUi

