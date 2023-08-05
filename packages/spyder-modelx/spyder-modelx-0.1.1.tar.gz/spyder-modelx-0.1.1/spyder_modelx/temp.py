from qtpy import QtCore, QtGui
from qtpy.QtWidgets import (
    QFileDialog, QApplication, QComboBox, QWidget, QPushButton, QMenuBar, QStatusBar, QMainWindow)
import pandas as pd

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self):
        self.comboData=['None']

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(456, 172)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(120, 60, 69, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.setEditable(True)
        self.comboBox.addItems(self.comboData)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 60, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.load)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 456, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Load", None))

    def load(self):
        fileName=QFileDialog.getOpenFileName(MainWindow,'Load File')
        data_pd=pd.read_csv(fileName,index_col=0,na_filter=False)
        self.comboData=list(data_pd.var1)
        print(self.comboData)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())