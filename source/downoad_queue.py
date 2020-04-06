# -*- coding: utf-8 -*-
# @author: YangLeiSX
# @data: 2020-04-06

from PyQt5 import QtCore
import os
from time import sleep


class DownoadQueue(QtCore.QThread):
    def __init__(self, parent, did, session, path, name, url, speed=500):
        super(DownoadQueue, self).__init__()
        self.parent = parent
        self.session = session
        self.path = path
        self.name = name
        self.url = url
        self.speed = speed
        self.did = did

    def run(self):
        self.parent.LogInfo.emit("[MSG]ID:{}\tBegin Download {}\n"
                                 .format(self.did, self.name))
        target = os.path.join(self.path, self.name)
        r = self.session.get(self.url, stream=True)
        with open("{}".format(target), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                sleep(1/self.speed)
        self.parent.LogInfo.emit("[MSG]ID:{}\tDownloads Finish\n"
                                 .format(self.did))
        self.parent.dq.pop(self.did)
        self.parent.DownloadFinish.emit()
