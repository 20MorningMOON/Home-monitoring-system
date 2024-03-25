import base64
import json
import random
import sys
import datetime
import asyncio
import time
import cv2
import numpy as np
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QInputDialog, QLineEdit
from monitorEach import Ui_MainWindow#注意这里的UI文件名及其class名，根据自己定义的来
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
from copy import deepcopy

thread_lock = threading.Lock()
thread_exit = False

#获取视频帧线程
class myThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(myThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    def getframe(self):
        return  deepcopy(self.frame)

    def run(self):
        global thread_exit
        begin_time=time.time()
        cap=cv2.VideoCapture(self.camera_id)
        end_time = time.time()
        print(end_time-begin_time)
        while not thread_exit:
            ret,frame=cap.read()
            k=0
            if ret:
                if k==0:
                    k=1
                    end_time = time.time()
                    print(end_time - begin_time)
                thread_lock.acquire()
                self.frame=frame
                thread_lock.release()
            else:
                thread_exit=True
        cap.release()

class MonitorEachMainWindowLocal(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None, token=None, user_id=None,cam_id=None,cam_name=None):
        super(MonitorEachMainWindowLocal, self).__init__(parent)
        self.setupUi(self)
        self.token = token
        self.user_id = user_id
        self.cam_id = cam_id
        self.setWindowTitle(f'摄像头实时画面')
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/monitor.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)
        self.frame=None
        self.title.setText(f'当前摄像头:{cam_name}')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_video)
        self.timer.start()


    def show_video(self):
        thread_lock.acquire()
        if self.frame is not None:
            self.show_cv_img(self.frame)
        thread_lock.release()

    def show_cv_img(self,img):
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        QtImg = QtGui.QImage(shrink.data,
                             shrink.shape[1],
                             shrink.shape[0],
                             shrink.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        jpg_out = QtGui.QPixmap(QtImg).scaled(self.videoLabel.width()-2, self.videoLabel.height()-2)
        self.videoLabel.setPixmap(jpg_out)

class MonitorEachMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None, token=None, user_id=None,cam_id=None,cam_name=None):
        super(MonitorEachMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.token = token
        self.user_id = user_id
        self.cam_id=cam_id
        self.setWindowTitle(f'摄像头实时画面')
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/monitor.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)
        self.title.setText(f'当前摄像头:{cam_name}')
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.show_video)
        # 视频链接由cam_id进行获取
        self.videolink=f'rtmp://43.143.245.240/live/stream{self.cam_id}?token={self.token}'
        self.childthread=myThread(self.videolink,self.videoLabel.height()-2,self.videoLabel.width()-2)
        self.childthread.setDaemon(True)
        self.childthread.start()
        self.timer.start(5)

    #信号
    my_Signal=QtCore.pyqtSignal(str)


    def show_video(self):
        thread_lock.acquire()
        frame=self.childthread.getframe()
        thread_lock.release()
        self.show_cv_img(frame)

    def show_cv_img(self,img):
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        QtImg = QtGui.QImage(shrink.data,
                             shrink.shape[1],
                             shrink.shape[0],
                             shrink.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        jpg_out = QtGui.QPixmap(QtImg).scaled(self.videoLabel.width()-2, self.videoLabel.height()-2)
        self.videoLabel.setPixmap(jpg_out)

    def closeEvent(self, event):
        self.my_Signal.emit(self.cam_id)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    token1='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIwMDUwNTZjMDAwMDgiLCJleHAiOjUwNTExMjkxNTYuMDMzMDI1fQ.tbl6oPBLtFl8oIDrl240itESMI3rmbVPRgegzVjoCuI'
    myWin = MonitorEachMainWindow(token=token1,user_id='user1',cam_id='2',cam_name='camTest')
    myWin.show()
    sys.exit(app.exec_())

# ffmpeg -r 30 -re -i - -vcodec h264 -max_delay 100 -f flv -g 5 -b 700000 rtmp://43.143.245.240/live/stream2?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIwMDUwNTZjMDAwMDgiLCJleHAiOjUwNTExMjkxNTYuMDMzMDI1fQ.tbl6oPBLtFl8oIDrl240itESMI3rmbVPRgegzVjoCuI