# -*- coding: utf-8 -*-
# @author: YangLeiSX
# @data: 2020-04-06

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.JaccountLabel = QtWidgets.QLabel(self.centralwidget)
        self.JaccountLabel.setObjectName("JaccountLabel")
        self.horizontalLayout_2.addWidget(self.JaccountLabel)
        self.Jaccount = QtWidgets.QLineEdit(self.centralwidget)
        self.Jaccount.setObjectName("Jaccount")
        self.horizontalLayout_2.addWidget(self.Jaccount)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.PasswordLabel = QtWidgets.QLabel(self.centralwidget)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.horizontalLayout_4.addWidget(self.PasswordLabel)
        self.Password = QtWidgets.QLineEdit(self.centralwidget)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password.setObjectName("Password")
        self.horizontalLayout_4.addWidget(self.Password)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.LocalPath = QtWidgets.QLineEdit(self.centralwidget)
        self.LocalPath.setObjectName("LocalPath")
        self.horizontalLayout_6.addWidget(self.LocalPath)
        self.GetPathBtn = QtWidgets.QPushButton(self.centralwidget)
        self.GetPathBtn.setObjectName("GetPathBtn")
        self.horizontalLayout_6.addWidget(self.GetPathBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.LoginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.LoginBtn.setObjectName("LoginBtn")
        self.horizontalLayout_5.addWidget(self.LoginBtn)
        self.UpdateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateBtn.setObjectName("UpdateBtn")
        self.horizontalLayout_5.addWidget(self.UpdateBtn)
        self.DownloadsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadsBtn.setObjectName("DownloadsBtn")
        self.horizontalLayout_5.addWidget(self.DownloadsBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.RemoteLabel = QtWidgets.QLabel(self.centralwidget)
        self.RemoteLabel.setObjectName("RemoteLabel")
        self.verticalLayout_5.addWidget(self.RemoteLabel)
        self.RemoteFile = QtWidgets.QTreeWidget(self.centralwidget)
        self.RemoteFile.setObjectName("RemoteFile")
        self.RemoteFile.headerItem().setText(0, "1")
        self.verticalLayout_5.addWidget(self.RemoteFile)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.LocalBabel = QtWidgets.QLabel(self.centralwidget)
        self.LocalBabel.setObjectName("LocalBabel")
        self.verticalLayout_4.addWidget(self.LocalBabel)
        self.LocalFile = QtWidgets.QTreeWidget(self.centralwidget)
        self.LocalFile.setObjectName("LocalFile")
        self.LocalFile.headerItem().setText(0, "1")
        self.verticalLayout_4.addWidget(self.LocalFile)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.Log = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Log.setObjectName("Log")
        self.verticalLayout.addWidget(self.Log)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setProperty("value", 24)
        self.progress.setObjectName("progress")
        self.horizontalLayout_7.addWidget(self.progress)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.JaccountLabel.setText(_translate("MainWindow", "Jaccoount"))
        self.PasswordLabel.setText(_translate("MainWindow", "Password"))
        self.GetPathBtn.setText(_translate("MainWindow", "..."))
        self.LoginBtn.setText(_translate("MainWindow", "Login"))
        self.UpdateBtn.setText(_translate("MainWindow", "Update"))
        self.DownloadsBtn.setText(_translate("MainWindow", "Downloads"))
        self.RemoteLabel.setText(_translate("MainWindow", "RemoteFile"))
        self.LocalBabel.setText(_translate("MainWindow", "LocalFile"))
