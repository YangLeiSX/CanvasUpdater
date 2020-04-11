# -*- coding: utf-8 -*-
# @author: YangLeiSX
# @data: 2020-04-06

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from ui_captcha import Ui_Captcha
import os


class Captcha(QtWidgets.QDialog, Ui_Captcha):
    def __init__(self):
        super(Captcha, self).__init__()
        self.setupUi(self)
        log_dir = os.path.join(
                       os.path.split(os.path.abspath(__file__))[0],
                       "log")
        pixmap = QtGui.QPixmap(os.path.join(log_dir, "captcha.jpeg"))
        self.captcha.setPixmap(pixmap)
        self.show()
