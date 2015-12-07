# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Fri Jun 26 09:54:41 2015
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(834, 617)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblWebcam = QtGui.QLabel(self.centralwidget)
        self.lblWebcam.setMinimumSize(QtCore.QSize(500, 500))
        self.lblWebcam.setSizeIncrement(QtCore.QSize(0, 0))
        self.lblWebcam.setBaseSize(QtCore.QSize(500, 500))
        self.lblWebcam.setObjectName(_fromUtf8("lblWebcam"))
        self.gridLayout.addWidget(self.lblWebcam, 2, 0, 1, 1)
        self.exitButton = QtGui.QPushButton(self.centralwidget)
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        self.gridLayout.addWidget(self.exitButton, 3, 1, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.upButton = QtGui.QPushButton(self.centralwidget)
        self.upButton.setEnabled(True)
        self.upButton.setObjectName(_fromUtf8("upButton"))
        self.gridLayout_2.addWidget(self.upButton, 4, 1, 1, 1)
        self.stopButtonKC = QtGui.QPushButton(self.centralwidget)
        self.stopButtonKC.setEnabled(True)
        self.stopButtonKC.setObjectName(_fromUtf8("stopButtonKC"))
        self.gridLayout_2.addWidget(self.stopButtonKC, 5, 1, 1, 1)
        self.downButton = QtGui.QPushButton(self.centralwidget)
        self.downButton.setEnabled(True)
        self.downButton.setObjectName(_fromUtf8("downButton"))
        self.gridLayout_2.addWidget(self.downButton, 6, 1, 1, 1)
        self.leftButton = QtGui.QPushButton(self.centralwidget)
        self.leftButton.setEnabled(True)
        self.leftButton.setObjectName(_fromUtf8("leftButton"))
        self.gridLayout_2.addWidget(self.leftButton, 5, 0, 1, 1)
        self.rightButton = QtGui.QPushButton(self.centralwidget)
        self.rightButton.setEnabled(True)
        self.rightButton.setObjectName(_fromUtf8("rightButton"))
        self.gridLayout_2.addWidget(self.rightButton, 5, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 2, 1, 1, 1)
        self.connectButton = QtGui.QPushButton(self.centralwidget)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.gridLayout.addWidget(self.connectButton, 0, 1, 1, 1)
        self.disconnectButton = QtGui.QPushButton(self.centralwidget)
        self.disconnectButton.setEnabled(True)
        self.disconnectButton.setObjectName(_fromUtf8("disconnectButton"))
        self.gridLayout.addWidget(self.disconnectButton, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Webcam viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.lblWebcam.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("MainWindow", "EXIT", None, QtGui.QApplication.UnicodeUTF8))
        self.upButton.setText(QtGui.QApplication.translate("MainWindow", "UP", None, QtGui.QApplication.UnicodeUTF8))
        self.stopButtonKC.setText(QtGui.QApplication.translate("MainWindow", "STOP", None, QtGui.QApplication.UnicodeUTF8))
        self.downButton.setText(QtGui.QApplication.translate("MainWindow", "DOWN", None, QtGui.QApplication.UnicodeUTF8))
        self.leftButton.setText(QtGui.QApplication.translate("MainWindow", "LEFT", None, QtGui.QApplication.UnicodeUTF8))
        self.rightButton.setText(QtGui.QApplication.translate("MainWindow", "RIGHT", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("MainWindow", "CONNECT", None, QtGui.QApplication.UnicodeUTF8))
        self.disconnectButton.setText(QtGui.QApplication.translate("MainWindow", "DISCONNECT", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

