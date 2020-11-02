from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(324, 234)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_select_button = QtWidgets.QPushButton(self.centralwidget)
        self.file_select_button.setGeometry(QtCore.QRect(30, 30, 251, 41))
        self.file_select_button.setObjectName("file_select_button")
        self.text_label_1 = QtWidgets.QLabel(self.centralwidget)
        self.text_label_1.setGeometry(QtCore.QRect(60, 100, 201, 31))
        self.text_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label_1.setObjectName("text_label_1")
        self.link_input = QtWidgets.QLineEdit(self.centralwidget)
        self.link_input.setGeometry(QtCore.QRect(30, 150, 261, 20))
        self.link_input.setObjectName("link_input")
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(110, 190, 75, 23))
        self.play_button.setObjectName("play_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scene Depiction"))
        self.file_select_button.setText(_translate("MainWindow", "Click here to Select Video from your PC"))
        self.text_label_1.setText(_translate("MainWindow", "Or Enter a link below and Click Play!"))
        self.play_button.setText(_translate("MainWindow", "Play!"))
        self.file_select_button.clicked.connect(self.file_select_handler)

    def file_select_handler(self):
        filename=QtWidgets.QFileDialog.getOpenFileName()
        self.path=filename[0]
        print(self.path)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
