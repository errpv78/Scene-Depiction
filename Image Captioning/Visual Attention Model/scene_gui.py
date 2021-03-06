from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import time
import pafy
import pyautogui
from pynput import keyboard
from pynput.keyboard import Key, Controller, Listener
import speech_recognition as sr
from gtts import gTTS
import vlc
from Visual_Attention_Model import evaluate, plot_attention
import time
import os
from Predict_cap import predict_caption



r = sr.Recognizer()
# keyboard = Controller()
mic = sr.Microphone()
count = 0

dirpath = os.path.dirname(os.path.abspath(__file__))
command = 'Command not found please speak again or try pressing space'
file = gTTS(text=command, lang='en')
file.save(dirpath + '/cmd.mp3')

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    global count, dirpath
    if key == keyboard.Key.space:
        count += 1
        if count%2==1:
            myScreenshot = pyautogui.screenshot()
            image_path = dirpath + '/temp.png'
            myScreenshot.save(image_path)
            result, attention_plot = evaluate(image_path)
            caption = ' '.join(result[:-1])
            # print(caption)
            caption = caption.replace('<unknown> ', '')
            caption = caption.replace('<unknown>', '')
            print(caption)
            file = gTTS(text=caption, lang='en')
            file.save('hello.mp3')
            p = vlc.MediaPlayer('hello.mp3')
            p.play()
            time.sleep(2)

            # while True:
            #     with mic as source:
            #         audio = r.listen(source)
            #     try:
            #         query = r.recognize_google(audio)
            #         print(query, query)
            #         if query=='play':
            #             Controller.press(Key.space)
            #             Controller.release(Key.space)
            #             break
            #     except Exception as e:
            #         print(e)
            #         p = vlc.MediaPlayer(dirpath+'/cmd.mp3')
            #         p.play()
            #         time.sleep(2)
            #         print('Command not found!!')




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
        self.text_label_1.setGeometry(QtCore.QRect(60, 100, 230, 32))
        self.text_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label_1.setObjectName("text_label_1")
        self.link_input = QtWidgets.QLineEdit(self.centralwidget)
        self.link_input.setGeometry(QtCore.QRect(30, 150, 261, 20))
        self.link_input.setObjectName("link_input")
        regex=QtCore.QRegExp(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")
        validator = QtGui.QRegExpValidator(regex)
        self.link_input.setValidator(validator)
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(50, 190, 75, 23))
        self.play_button.setObjectName("play_button")
        self.help_button = QtWidgets.QPushButton(self.centralwidget)
        self.help_button.setGeometry(QtCore.QRect(184, 190, 75, 23))
        self.play_button.setObjectName("play_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scene Depiction"))
        self.file_select_button.setText(_translate("MainWindow", "Click here to Select Video from your PC"))
        self.text_label_1.setText(_translate("MainWindow", "Or Enter YouTube video link below"))
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.help_button.setText(_translate("MainWindow", "Scene Caption Mode"))
        self.file_select_button.clicked.connect(self.file_select_handler)
        self.play_button.clicked.connect(self.play_video)
        self.help_button.clicked.connect(self.help_dialog)

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

    def help_dialog(self):
        dialog=QtWidgets.QDialog()
        dialog.setWindowTitle("Help Menu")
        self.text_label_2 = QtWidgets.QLabel(dialog)
        self.text_label_2.setGeometry(QtCore.QRect(60, 100, 330, 32))
        self.text_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label_2.setObjectName("text_label_2")
        self.text_label_2.setText("Video Assistance Model is on!")
        dialog.exec_()
        while True:
            with Listener(
                    on_press=on_press,
                    on_release=on_release) as listener:
                listener.join()


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
        frame_no = 0
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                frame_no+=1
                self.change_pixmap_signal.emit(cv_img)
                if frame_no == 50:
                    caption = predict_caption(cv_img)
                    print(caption)
                    caption = caption.replace('<unknown> ', '')
                    caption = caption.replace('<unknown>', '')
                    print(caption)
                    # sleep(3)
                    file = gTTS(text=caption, lang='en')
                    file.save('hello.mp3')
                    p = vlc.MediaPlayer('hello.mp3')
                    p.play()
                    time.sleep(2)
                    frame_no = 0

                time.sleep(0.033)
        cap.release()


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Player")
        self.disply_width = 640
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
