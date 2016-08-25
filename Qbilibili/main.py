# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'browser.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QTabBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets


class Signals(QObject):
    line_edit_text_change = pyqtSignal(QUrl)
    tab_activated = pyqtSignal(int)
    change_window_title = pyqtSignal(str)
    link_hovered = pyqtSignal(str)
    load_url = pyqtSignal(str)
    video_window_closed = pyqtSignal()

_gSignals = Signals()

from player import VideoPlayer


class TabBar(QTabBar):

    def __init__(self, parent):
        super(TabBar, self).__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(parent.closeTab)
        self.currentChanged.connect(self.tabActivated)

    def tabActivated(self, index):
        print(index)
        _gSignals.tab_activated.emit(index)


class TabWidget(QTabWidget):

    def __init__(self, parent):
        super(TabWidget, self).__init__(parent)
        self.resize(640, 480)
        self.setTabBar(TabBar(self))

        _gSignals.tab_activated.connect(self.tab_activated)
        _gSignals.load_url.connect(self.load_url)

        web_view = self.create_new_tab()
        web_view.home_page()

    def closeTab(self, index):
        self.removeTab(index)

    def request_new_tab(self):
        return self.create_new_tab()

    def webview_title_changed(self):
        sender = self.sender()
        title = sender.title()
        print(title)
        index = self.indexOf(sender)
        self.setTabText(index, title)
        _gSignals.change_window_title.emit(title)

    def webview_url_changed(self):
        sender = self.sender()
        index = self.indexOf(sender)
        if (self.currentIndex() == index):
            _gSignals.line_edit_text_change.emit(sender.url())

    def tab_activated(self, index):
        web_view = self.widget(index)
        if not web_view:
            return
        _gSignals.line_edit_text_change.emit(web_view.url())
        _gSignals.change_window_title.emit(web_view.title())

    def link_hovered_emit(self, url):
        if url:
            _gSignals.link_hovered.emit(url)

    def create_new_tab(self):
        web_view = self.create_web_view()
        self.addTab(web_view, "Untitled")
        self.setCurrentWidget(web_view)
        return web_view

    def create_web_view(self):
        web_view = WebView(self.request_new_tab)
        web_view.titleChanged.connect(self.webview_title_changed)
        web_view.urlChanged.connect(self.webview_url_changed)
        web_view.page().linkHovered.connect(self.link_hovered_emit)
        return web_view

    def load_url(self, url):
        index = self.currentIndex()
        web_view = self.widget(index)
        if not web_view:
            web_view = self.create_web_view()
        web_view.setUrl(QUrl(url))


class WebView(QWebEngineView):

    def __init__(self, new_tab_callback, loadHomePage=False):
        super(WebView, self).__init__()
        page = QWebEnginePage()
        self.setPage(page)
        if loadHomePage:
            self.home_page()
        self.next_url = ""
        self.new_tab_callback = new_tab_callback

    def home_page(self):
        # self.setUrl(QUrl("http://live.bilibili.com/single"))
        self.setUrl(QUrl("http://live.bilibili.com/12265"))

    def set_statubar_url(self, url):
        # print (url)
        self.next_url = url

    def createWindow(self, _type):
        return self.new_tab_callback()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.connections()
        self.video_player = VideoPlayer()
        self.window_title = "Qbilibili"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(12, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = TabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 713, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "go"))
        self.pushButton_2.setText(_translate("MainWindow", "play"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def connections(self):
        self.lineEdit.returnPressed.connect(self.lineEditReturnPressed)
        self.pushButton.clicked.connect(self.lineEditReturnPressed)
        _gSignals.line_edit_text_change.connect(self.lineEditTextChange)
        _gSignals.change_window_title.connect(self.change_window_title)
        _gSignals.link_hovered.connect(self.link_hovered_handler)
        self.pushButton_2.clicked.connect(self.play_button_pushed)

    def lineEditReturnPressed(self):
        url = self.lineEdit.text()
        if url:
            _gSignals.load_url.emit(url)

    def lineEditTextChange(self, url):
        self.lineEdit.setText(url.url())

    def change_window_title(self, title):
        self.setWindowTitle("%s - [ Qbilibili ]" % title)
        self.window_title = title

    def link_hovered_handler(self, url):
        self.statusbar.showMessage(url, 1000)

    def play_button_pushed(self):
        self.video_player.play(str(self.lineEdit.text()), self.window_title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    view = MainWindow()
    view.show()
    sys.exit(app.exec_())
