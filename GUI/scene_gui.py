from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import time
import pafy


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
        regex=QtCore.QRegExp(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")
        validator = QtGui.QRegExpValidator(regex)
        self.link_input.setValidator(validator)
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
        self.play_button.clicked.connect(self.play_video)

    def file_select_handler(self):
        filename=QtWidgets.QFileDialog.getOpenFileName()
        self.path=filename[0]

    def play_video(self):
        self.url_present=False
        if self.link_input.text():
            self.url_present=True
            self.url=self.link_input.text()
        self.a=App()
        self.a.show()

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        if ui.url_present:
            vPafy=pafy.new(ui.url)
            play=vPafy.getbest()
            cap=cv2.VideoCapture(play.url)
            ui.url_present=False
        else:
            cap = cv2.VideoCapture(ui.path)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                time.sleep(0.033)
        cap.release()


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QT CV")
        self.disply_width = 840
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)

        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
