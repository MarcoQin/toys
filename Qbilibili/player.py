#!/usr/bin/env python
# encoding: utf-8

import os
import time
from threading import Thread
import mpv1 as mpv
from danmu import DanMuClient
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QTabBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets

from bilibili import Bilibili
from danmaku2ass_min import WriteComment, WriteASSHead

cur_dir = os.path.abspath(os.path.dirname(__file__))


class Signals(QObject):
    video_window_closed = pyqtSignal()

_gSignals = Signals()


class VideoWindow(QWidget):

    def __init__(self, close_callback):
        super(VideoWindow, self).__init__()
        self.resize(1024, 768)
        self.close_callback = close_callback

    def closeEvent(self, event=None):
        #  print ('video_window_closed_handler emit!')
        #  _gSignals.video_window_closed.emit()
        self.close_callback()


#  class VideoPlayer(QObject):
class VideoPlayer(object):

    def __init__(self):
        self.video_window = VideoWindow(self.video_window_closed_handler)
        import locale
        locale.setlocale(locale.LC_NUMERIC, "C")
        self.mpv = mpv.MPV(
            wid=str(int(self.video_window.winId())),
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="1000",
            #  input_cursor="no",
            input_cursor="yes",
            input_default_bindings="no",
            config="yes",
            config_dir=cur_dir,
            hwdec="videotoolbox",
            #  display_fps="60",
        )
        self.danmaku_client = None
        self.danmaku_fd = None
        self.sub_loded = False
        self.cache = []
        self.sub_alive = False
        #  _gSignals.video_window_closed.connect(self.video_window_closed_handler)

    def play(self, url, title=""):
        self.init_danmaku(url)
        url = Bilibili.get_live_address(url, index=2)
        print (url)
        self.mpv.command("loadfile", url)
        self.video_window.show()
        self.video_window.setWindowTitle(title)

    def video_window_closed_handler(self):
        print ('video_window_closed_handler')
        self.sub_alive = False
        self.mpv.command("stop")
        if self.danmaku_client:
            self.danmaku_client.stop()
        self.danmaku_client = None
        if self.danmaku_fd:
            self.danmaku_fd.close()
        self.sub_loded = False
        self.cache[:] = []

    def sub_add(self, filename):
        self.mpv.command("sub-add", filename)

    def sub_reload(self):
        self.mpv.command("sub-reload")

    def init_danmaku(self, url):
        print("init_danmaku")
        print(type(url))
        print(url)

        self.danmaku_client = DanMuClient(url)
        self.danmaku_client.danmu(self.handle_danmu)
        self.danmaku_client.start()

        self.danmaku_fd = open("danmaku_temp.ass", "w")
        width = 1280
        height = 720
        #  fontface = "STHeiti"
        #  fontface = "Arial Unicode"
        fontface = "Kaiti"
        #  fontsize = 24
        self.fontsize = 30
        #  alpha = 0.7
        alpha = 1
        styleid = "test"
        WriteASSHead(self.danmaku_fd, width=width, height=height, fontface=fontface, fontsize=self.fontsize, alpha=alpha, styleid=styleid)
        WriteComment(self.danmaku_fd, "welcome", 1, 0, width, 3, "test")
        self.danmaku_fd.close()

    def reload_sub_schedule(self):
        while self.sub_alive:
            time.sleep(1)
            self.sub_reload()

    def handle_danmu(self, danmu):
        t = self.mpv.time_pos
        if not t:
            return
        if not self.sub_loded:
            self.mpv.sub_add("danmaku_temp.ass")
            self.sub_loded = True
            thread = Thread(target=self.reload_sub_schedule)
            self.sub_alive = True
            thread.start()
        text = danmu['Content']
        # print(text, len(text))
        width = 1280
        row = 10
        valid_row = self.danmaku_engine(t, len(text) * 4)
        self.danmaku_fd = open("danmaku_temp.ass", "a")
        WriteComment(self.danmaku_fd, text, t, valid_row, width, 10, "test")
        self.danmaku_fd.close()
        #  self.mpv.sub_reload()

    def danmaku_engine(self, t, length):
        font_size = 24
        font_size = self.fontsize
        danmaku = {
            "t": t,
            "len": length,
            "row": 10,
            "speed": length / (16 / font_size),
        }
        valid_row = None


        index = 0

        for i, danmu in enumerate(self.cache):
            t1 = t - danmu['t']
            # print("speed", danmu["speed"])
            l = t1 * danmu['speed']
            # print("l", l)
            # print("len", danmu['len'])
            if l > danmu['len']:
                # print("l > len")
                valid_row = danmu['row']
                # print("valid row", valid_row)
                index = i
                break

        if valid_row is not None:
            danmaku['row'] = valid_row
            self.cache.pop(index)
            self.cache.append(danmaku)
            return valid_row
        else:
            if len(self.cache) > 10:
                first = self.cache.pop(0)
                valid_row= first['row']
                danmaku['row'] = valid_row
                self.cache.append(danmaku)
                return valid_row
            else:
                valid_row = (len(self.cache) + 0) * 36
                danmaku['row'] = valid_row
                self.cache.append(danmaku)
                return valid_row

