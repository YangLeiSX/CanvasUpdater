# -*- coding: utf-8 -*-
# @author: YangLeiSX
# @data: 2020-04-06

import sys
import os
import json
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import qDebug, QFileInfo
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import QApplication, QMainWindow,\
                QFileDialog, QTreeWidgetItem, QFileIconProvider
from ui_mainwindow import Ui_MainWindow
# from captcha import Captcha
from credential import login
from canvas_update import CanvasUpdate
from downoad_queue import DownoadQueue


class MainWindow(QMainWindow, Ui_MainWindow):
    LogInfo = Signal(str)
    FetchFinish = Signal()
    DownloadFinish = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.session = None
        self.cu = None
        self.path = None
        self.dq = {}
        self.log_dir = os.path.join(
                       os.path.split(os.path.abspath(__file__))[0],
                       "log")

        self.FetchFinish.connect(self.parseRemote)
        self.LogInfo.connect(self.logInfo)
        self.DownloadFinish.connect(self.parseLocal)

        self.initRender()
        if self.parseRemote():
            self.LogInfo.emit("[MSG]Load Cache Successfully!\n")

    def initRender(self):
        self.setupUi(self)
        self.LocalPath.setText("Select Your Local Path")
        self.Log.setPlainText("[DEBUG]System Begin\n")
        self.progress.setValue(0)
        if os.path.exists(os.path.join(self.log_dir, 'loginInfo.json')):
            with open(os.path.join(self.log_dir, 'loginInfo.json'), 'r') as f:
                loginInfo = json.loads(f.read())
                self.Jaccount.setText(loginInfo['jaccount'])
                self.Password.setText(loginInfo['password'])

    @Slot()
    def on_LoginBtn_clicked(self):
        if self.session:
            self.session.close()
            self.seesion = None
        jaccount = self.Jaccount.text()
        password = self.Password.text()
        if (not jaccount) or (not password):
            return
        qDebug(jaccount)
        qDebug(password)
        self.session = login(url="https://oc.sjtu.edu.cn/login/openid_connect",
                             parent=self, username=jaccount, password=password)
        if self.session:
            self.LogInfo.emit("[MSG]Log in Successfully!\n")
            loginInfo = {}
            loginInfo['jaccount'] = jaccount
            loginInfo['password'] = password
            with open(os.path.join(self.log_dir, 'loginInfo.json'), 'w') as f:
                f.write(json.dumps(loginInfo))
        else:
            self.LogInfo.emit("[ERROR]Log in Fail!\n")

    @Slot()
    def on_UpdateBtn_clicked(self):
        if not self.session:
            self.LogInfo.emit("[ERROR]Please Log in!\n")
            return
        self.cu = CanvasUpdate(self, self.session)
        self.cu.start()
        self.parseRemote()

    @Slot()
    def on_GetPathBtn_clicked(self):
        filepath = QFileDialog.getExistingDirectory(self,
                                                    'Select Your Local Path',
                                                    '.')
        if filepath:
            # qDebug(filepath)
            self.path = filepath
            self.LocalPath.setText(filepath)
            self.parseLocal()

    @Slot()
    def on_DownloadsBtn_clicked(self):
        if not self.session:
            self.LogInfo.emit("[ERROR]Please Log in!\n")
            return
        if not self.path:
            self.LogInfo.emit("[ERROR]Please select path!\n")
            return
        selectList = self.RemoteFile.selectedItems()
        try:
            file_path = self.LocalFile.selectedItems()[0].text(1)
        except IndexError:
            file_path = self.path
        for selected in selectList:
            did = len(self.dq)
            while did in self.dq:
                did = did+1
            dq = DownoadQueue(self, did=did, session=self.session,
                              path=file_path, name=selected.text(0),
                              url=selected.text(1))
            self.dq[did] = dq
            dq.start()

    def logInfo(self, message):
        raw = self.Log.toPlainText()
        self.Log.setPlainText(str(raw)+message)
        self.Log.moveCursor(self.Log.textCursor().End)

    def parseRemote(self):
        self.RemoteFile.clear()
        if not os.path.exists(os.path.join(self.log_dir, 'file_tree.json')):
            return None
        with open(os.path.join(self.log_dir, 'file_tree.json'), 'r') as f:
            file_tree = json.loads(f.read())
        with open(os.path.join(self.log_dir, 'courses.json'), 'r') as f:
            courses_name = json.loads(f.read())
        root = QTreeWidgetItem(self.RemoteFile)
        root.setText(0, "Remote Files")
        # courseItem = []
        for i, (k, v) in enumerate(file_tree.items()):
            tmp = QTreeWidgetItem(root)
            tmp.setText(0, courses_name[k])
            # courseItem.append(tmp)
            for item in v:
                try:
                    item['content']
                except KeyError:
                    self.parseFile(tmp, item)
                else:
                    self.parseFolder(tmp, item)

    def parseFile(self, parent, adict):
        # qDebug("it is a file")
        tmp = QTreeWidgetItem(parent)
        tmp.setText(0, adict['name'])
        tmp.setText(1, adict['url'])

    def parseFolder(self, parent, alist):
        # qDebug("it is a folder")
        tmp = QTreeWidgetItem(parent)
        tmp.setText(0, alist['name'])
        if not isinstance(alist['content'], list):
            return
        for item in alist['content']:
            try:
                item['content']
            except KeyError:
                self.parseFile(tmp, item)
            else:
                self.parseFolder(tmp, item)

    def parseLocal(self):
        localpath = self.path
        self.LocalFile.clear()
        root = QTreeWidgetItem(self.LocalFile)
        root.setText(0, "Local Files")
        root.setText(1, localpath)
        for item in os.listdir(localpath):
            item_path = os.path.join(localpath, item)
            if os.path.isdir(item_path):
                self.parseLocalDir(parent=root, name=item, path=item_path)
            if os.path.isfile(item_path):
                self.parseLocalFile(parent=root, name=item, path=item_path)

    def parseLocalDir(self, parent, name, path):
        tmp = QTreeWidgetItem(parent)
        fileInfo = QFileInfo(path)
        fileIcon = QFileIconProvider()
        icon = QIcon(fileIcon.icon(fileInfo))
        tmp.setIcon(0, QIcon(icon))
        tmp.setText(0, name)
        tmp.setText(1, path)
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                self.parseLocalDir(parent=tmp, name=item, path=item_path)
            if os.path.isfile(item_path):
                self.parseLocalFile(parent=tmp, name=item, path=item_path)

    def parseLocalFile(self, parent, name, path):
        if name[0] == '.':
            return
        tmp = QTreeWidgetItem(parent)
        fileInfo = QFileInfo(path)
        fileIcon = QFileIconProvider()
        icon = QIcon(fileIcon.icon(fileInfo))
        tmp.setIcon(0, QIcon(icon))
        tmp.setText(0, name)
        tmp.setText(1, os.path.split(path)[0])


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
