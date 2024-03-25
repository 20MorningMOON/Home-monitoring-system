import json
import sys
import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QInputDialog, QLineEdit
from monitorMenu import Ui_MainWindow#注意这里的UI文件名及其class名，根据自己定义的来
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
import requests
import menu_main
import monitorEach_main
from headers_list import headers_list

class MonitorMenuMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None,token=None,user_id=None):
        super(MonitorMenuMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width,self.height)
        self.token = token
        self.user_id = user_id
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        self.cam_name_id = {}
        self.watch_name_id = {}
        self.cam_id_no={}
        self.watch_id_no={}
        self.watchwin=[]
        self.camwin=[]
        self.watchno=0
        self.camno=0
        with open("resource/share.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)
        # self.back.clicked.connect(self.backMenu)
        self.playWatch.clicked.connect(self.playWatchByBox)
        self.playCam.clicked.connect(self.playCamByBox)
        self.initWatchBox()
        self.initCamBox()



    def initWatchBox(self):
        headers = random.choice(headers_list)
        response = requests.get('http://43.143.245.240:8000/watchlist?token=' + self.token,headers=headers)
        response = json.loads(response.text)
        data = response['data']
        self.watchBox.addItem('请选择')
        for i,d in enumerate(data):
            self.watchBox.addItem(str(d['cam__name']))
            self.watch_name_id[str(d['cam__name'])] = str(d['cam__id'])


    def initCamBox(self):
        headers = random.choice(headers_list)
        response = requests.get('http://43.143.245.240:8000/camlist?token=' + self.token, headers=headers)
        response = json.loads(response.text)
        data = response['data']
        self.camBox.addItem('请选择')
        for i,d in enumerate(data):
            self.camBox.addItem(str(d['name']))
            self.cam_name_id[str(d['name'])] = str(d['id'])

    def playWatchByBox(self):
        if self.watchBox.currentText()=='请选择':
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头！')
            return None
        #获取id
        tmp1=self.watch_name_id[self.watchBox.currentText()]
        #判断是否推流
        ifstream = json.loads((requests.post('http://43.143.245.240:8000/ifstream/', data={'token':self.token,'cam_id':tmp1}).text))['status']
        if ifstream=='no streaming':
            QMessageBox.critical(self, '提示', '当前摄像头不处于工作状态')
            return None
        #id不在字典中
        if not tmp1 in self.watch_id_no:
            self.watch_id_no[tmp1]=self.watchno
            self.watchwin.append(monitorEach_main.MonitorEachMainWindow(token=self.token,user_id=self.user_id,cam_id=tmp1,cam_name=self.watchBox.currentText()))
            # 此处添加信号
            self.watchwin[self.watchno].my_Signal.connect(self.child_exit)
            self.watchwin[self.watchno].show()
            self.watchno+=1
        # id在字典中
        else:
            tmp2=self.watch_id_no[tmp1]
            self.watchwin[tmp2]=monitorEach_main.MonitorEachMainWindow(token=self.token,user_id=self.user_id,cam_id=tmp1,cam_name=self.watchBox.currentText())
            #此处添加信号
            self.watchwin[tmp2].my_Signal.connect(self.child_exit)
            self.watchwin[tmp2].show()
    def playCamByBox(self):
        if self.camBox.currentText()=='请选择':
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头！')
            return None
        # 获取id
        tmp1 = self.cam_name_id[self.camBox.currentText()]
        # 判断是否推流
        ifstream = json.loads(
            (requests.post('http://43.143.245.240:8000/ifstream/', data={'token': self.token, 'cam_id': tmp1}).text))[
            'status']
        if ifstream == 'no streaming':
            QMessageBox.critical(self, '提示', '当前摄像头不处于工作状态')
            return None
        # id不在字典中
        if not tmp1 in self.cam_id_no:
            self.cam_id_no[tmp1] = self.camno
            self.camwin.append(
                monitorEach_main.MonitorEachMainWindow(token=self.token, user_id=self.user_id, cam_id=tmp1,cam_name=self.camBox.currentText()))
            # 此处添加信号
            self.camwin[self.camno].my_Signal.connect(self.child_exit)
            self.camwin[self.camno].show()
            self.camno += 1
        # id在字典中
        else:
            tmp2 = self.cam_id_no[tmp1]
            self.camwin[tmp2] = monitorEach_main.MonitorEachMainWindow(token=self.token, user_id=self.user_id,
                                                                         cam_id=tmp1,cam_name=self.camBox.currentText())
            # 此处添加信号
            self.camwin[tmp2].my_Signal.connect(self.child_exit)
            self.camwin[tmp2].show()

    #子窗口退出，删除相关窗口
    def child_exit(self,id):
        if id in self.cam_id_no:
            i = self.cam_id_no[id]
            self.camwin[i] = None
        else:
            i=self.watch_id_no[id]
            self.watchwin[i]=None


    def closeEvent(self, event):
        for p in self.camwin:
            if p is not None:
                p.close()
        for p in self.watchwin:
            if p is not None:
                p.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    token1='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIwMDUwNTZjMDAwMDgiLCJleHAiOjUwNTExMjkxNTYuMDMzMDI1fQ.tbl6oPBLtFl8oIDrl240itESMI3rmbVPRgegzVjoCuI'
    myWin = MonitorMenuMainWindow(token=token1)
    myWin.show()
    sys.exit(app.exec_())