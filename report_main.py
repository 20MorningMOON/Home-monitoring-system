import base64
import json
import random
import sys
import datetime
import asyncio

import requests
import websockets
from PyQt5.QtWidgets import *
import cv2
import numpy as np
import threading
import onnxruntime
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QInputDialog, QLineEdit
from report import Ui_MainWindow#注意这里的UI文件名及其class名，根据自己定义的来
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap

class ReportMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None, token=None):
        super(ReportMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width,self.height)
        self.token = token
        self.cam_name_id={}
        self.camcurrent_name=None
        self.camcurrent_id=None
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/report.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)
        self.initComboBox()
        self.queryBtn.clicked.connect(self.query)
        self.downloadBtn.clicked.connect(self.download)

    def initComboBox(self):
        self.cameraComboBox.addItem('请选择')
        response = requests.get('http://43.143.245.240:8000/camlist?token=' + self.token)
        response = json.loads(response.text)
        data=response['data']
        for d in data:
            self.cameraComboBox.addItem(str(d['name']))
            self.cam_name_id[str(d['name'])]=str(d['id'])
        response = requests.get('http://43.143.245.240:8000/watchlist?token=' + self.token)
        response = json.loads(response.text)
        data = response['data']
        for d in data:
            self.cameraComboBox.addItem(str(d['cam__name']))
            self.cam_name_id[str(d['cam__name'])]=str(d['cam__id'])

    def query(self):
        if self.cameraComboBox.currentText() == '请选择':
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头')
            return None
        self.camcurrent_name = self.cameraComboBox.currentText()
        self.camcurrent_id = self.cam_name_id[self.camcurrent_name]
        self.label_6.setText(f'当前摄像头:{self.camcurrent_name}')
        response=requests.post('http://43.143.245.240:8000/getevent/', data={'token': self.token, 'cam_id': self.camcurrent_id,'event_id':'0'})
        event = json.loads(response.text)['event']
        event.reverse()
        self.history.setRowCount(len(event))
        self.event_id=[]
        self.pic_exist=[]
        x=0
        for e in event:
            self.event_id.append(e['id'])
            if e['detail'] == 'fire':
                self.history.setItem(x,0,QtWidgets.QTableWidgetItem('火情'))
            elif e['detail'] == 'smoke':
                self.history.setItem(x,0,QtWidgets.QTableWidgetItem('烟雾'))
            else:
                self.history.setItem(x,0,QtWidgets.QTableWidgetItem('陌生人'))
            self.history.setItem(x, 1, QtWidgets.QTableWidgetItem(str(e['time'][:19].replace('T',' '))))
            if e['image']=='':
                self.history.setItem(x, 2, QtWidgets.QTableWidgetItem('无'))
                self.pic_exist.append(False)
            else:
                self.history.setItem(x, 2, QtWidgets.QTableWidgetItem('有'))
                self.pic_exist.append(True)
            x+=1

    def download(self):
        if self.camcurrent_id is None:
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头')
            return None
        if self.eventno.text() is None or self.eventno=='':
            return None
        if not self.eventno.text().isdigit():
            QMessageBox.critical(self, '查找失败', '输入序号不合法')
            return None
        eventno=int(self.eventno.text())
        if (eventno-1)>=0 and (eventno-1)<len(self.event_id):
            if not self.pic_exist[eventno-1]:
                QMessageBox.critical(self, '查找失败', '序号对应的事件无图片记录')
                return None
            else:
                #下载图片
                response = requests.get(f'http://43.143.245.240:8000/downloadeventimage?token={self.token}&event_id={self.event_id[eventno-1]}', stream=True)
                if response.headers['Content-Type'] == 'application/octet-stream':
                    open('resource/tmp.jpg', 'wb').write(response.content)  # 将内容写入图片
                    self.pic.setPixmap(QtGui.QPixmap('resource/tmp.jpg'))
                    self.pic.setScaledContents(True)
                else:
                    print(response.text)
        else:
            QMessageBox.critical(self, '下载失败', '输入序号不合法')
            return None




if __name__ == "__main__":
    app = QApplication(sys.argv)
    token2='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIxNGY2ZDg3ZTkxYzMiLCJleHAiOjUwNTI4OTk1MDUuMzE1NjM2fQ.nUDSB_AEOHoH7epU-CHPO-wOEuG-jrdzN-BSTNj7YmM'
    myWin = ReportMainWindow(token=token2)
    myWin.show()
    sys.exit(app.exec_())