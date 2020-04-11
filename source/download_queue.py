from PyQt5 import QtCore
import os
from time import sleep


class DownloadQueue(QtCore.QThread):
    def __init__(self, parent, did, session, path, name,
                 url, force=False, speed=500):
        super(DownloadQueue, self).__init__()
        self.parent = parent
        self.session = session
        self.path = path
        self.name = name
        self.url = url
        self.force = force
        self.speed = speed
        self.did = did

    def run(self):
        if not self.force:
            self.parent.LogInfo.emit("[MSG]ID:{}\tBegin Download {}\n"
                                     .format(self.did, self.name))
        target = os.path.join(self.path, self.name)
        r = self.session.get(self.url, stream=True)
        if not self.force:
            try:
                with open("{}".format(target), 'xb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                        if self.speed != 0:
                            sleep(1/self.speed)
            except FileExistsError:
                self.parent.LogInfo.emit("[ERROR]ID:{}\tFile Already Exists!\n"
                                         .format(self.did))
                self.parent.dq.pop(self.did)
                self.parent.ExistedFile.emit(self.path, self.name, self.url)
                return
            else:
                self.parent.LogInfo.emit("[MSG]ID:{}\tDownloads Finish\n"
                                         .format(self.did))
                self.parent.dq.pop(self.did)
                self.parent.DownloadFinish.emit()
                return
        else:
            self.parent.LogInfo.emit("[MSG]ID:{}\tWaiting to Download {}...\n"
                                     .format(self.did, self.name))
            while(len(self.parent.dq)) > 1:
                sleep(1)
            self.parent.LogInfo.emit("[MSG]Begin to Downloads {}\n"
                                     .format(self.name))
            with open("{}".format(target), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                    if self.speed != 0:
                        sleep(1/self.speed)
            self.parent.LogInfo.emit("[MSG]ID:{}\tReplace Finish!\n"
                                     .format(self.did))
            self.parent.dq.pop(self.did)
            self.parent.DownloadFinish.emit()
            return
