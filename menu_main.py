import os
import random
import sys
import threading
from copy import deepcopy

import cv2
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLineEdit
from psutil import net_if_addrs
from PyQt5 import QtCore, QtGui, QtWidgets
from menu import Ui_MainWindow
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
import requests
import monitorMenu_main
import edit_main
import share_main
import addface_main
from threading import Thread
from PushUtil import push_frame
import report_main, monitorEach_main
from headers_list import headers_list
import websockets
import json
import asyncio
import os
thread_lock = threading.Lock()

class myThread(threading.Thread):
    def __init__(self,token=None):
        super(myThread, self).__init__()
        self.token=token
        self.returnmsg=''

    async def receive(self, uri):
        async with websockets.connect(uri) as websocket:
            while True:
                recv_text = await websocket.recv()
                recvtext = json.loads(recv_text)
                print(recvtext)
                if recvtext['form']=='stream_start':
                    recvtext = recvtext['data']
                    msg=f"{recvtext['cam_id']}+{recvtext['token']}"
                    thread_lock.acquire()
                    self.returnmsg = msg
                    thread_lock.release()
                elif recvtext['form']=='stream_off':
                    recvtext = recvtext['data']
                    msg=f"+{recvtext['cam_id']}+{recvtext['cam_name']}"
                    thread_lock.acquire()
                    self.returnmsg = msg
                    thread_lock.release()
                elif recvtext['form'] == 'stream_on':
                    recvtext = recvtext['data']
                    msg = f"-{recvtext['cam_id']}+{recvtext['cam_name']}"
                    thread_lock.acquire()
                    self.returnmsg = msg
                    thread_lock.release()
                elif recvtext['form'] == 'event':
                    recvtext = recvtext['data']
                    if recvtext['detail'] == 'fire':
                        msg = f"摄像头({recvtext['cam_name']})疑似出现火情\n时间点{recvtext['time'][:19]}"
                        # print(msg)
                        thread_lock.acquire()
                        self.returnmsg=msg
                        thread_lock.release()
                    elif recvtext['detail'] == 'smoke':
                        msg = f"摄像头({recvtext['cam_name']})疑似出现烟雾\n时间点{recvtext['time'][:19]}"
                        # print(msg)
                        thread_lock.acquire()
                        self.returnmsg = msg
                        thread_lock.release()
                    else:
                        msg = f"摄像头({recvtext['cam_name']})疑似有陌生人\n时间点{recvtext['time'][:19]}"
                        # print(msg)
                        thread_lock.acquire()
                        self.returnmsg = msg
                        thread_lock.release()

    def recv(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.receive(f'ws://43.143.245.240:8000/ws/event/{self.token}/'))

    def run(self):
        self.recv()

    def getmsg(self):
        return deepcopy(self.returnmsg)


class MenuMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None,token=None,user_id=None):
        super(MenuMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(430,425)
        self.token=token
        self.user_id=user_id
        self.monitor.clicked.connect(self.showMonitors)
        self.edit.clicked.connect(self.toEditMonitors)
        self.share.clicked.connect(self.toShareMonitors)
        self.report.clicked.connect(self.toReport)
        self.addface.clicked.connect(self.toAddFace)
        self.openPush.clicked.connect(self.toAddCam)
        self.localwatch.clicked.connect(self.toCam)
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/logreg.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)
        self.monitorMenu_win =None
        self.local_cam_id=None
        self.edit_win=None
        self.share_win=None
        self.report_win=None
        self.addface_win=None
        self.watch=None
        self.msg=''
        self.push_flag=False
        self.countTimer = QtCore.QTimer()
        self.countTimer.timeout.connect(self.showMsg)
        # 接收信息子线程
        self.recvchild = myThread(token=self.token)
        self.recvchild.setDaemon(True)
        self.recvchild.start()
        #推流子线程
        self.pushchild=None

        mac = set()
        for k, v in net_if_addrs().items():
            for item in v:
                address = item[1]
                if '-' in address and len(address) == 17:
                    address = address.replace('-', '').lower()
                    mac.add(address)
        for cam in json.loads(requests.get('http://43.143.245.240:8000/camlist?token=' + self.token).text)['data']:
            # 说明在本设备上已经注册过，因此需要推流
            if cam['mac'] in mac:
                self.openPush.setText( "开启推流")
                self.openPush.clicked.disconnect(self.toAddCam)
                self.openPush.clicked.connect(lambda : self.toPush(str(cam['name']),str(cam['id'])))
                self.local_cam_id=str(cam['id'])
                break
        self.countTimer.start(100)


    def showMsg(self):
        thread_lock.acquire()
        if self.msg!=self.recvchild.getmsg():
            self.msg = self.recvchild.getmsg()
            if self.msg.startswith('摄像头'):
                QMessageBox.warning(self, '有异常情况', self.msg+'\n请打开报警记录界面查看')
            elif self.msg.startswith('+'):
                p = self.msg[1:]
                p = p.split('+')
                if p[0]==self.local_cam_id and self.openPush.text()=='关闭推流':
                    self.openPush.animateClick(500)
                else:
                    QMessageBox.information(self, '视频下线提醒', f'摄像头{p[1]}已下线')
            elif self.msg.startswith('-'):
                p=self.msg[1:]
                p = p.split('+')
                if not p[0] == self.local_cam_id:
                    QMessageBox.information(self, '视频上线提醒', f'摄像头{p[1]}已上线')
            else:
                p=self.msg.split('+')
                if p[0]==self.local_cam_id and p[1]==self.token and self.openPush.text()=='开启推流':
                    self.openPush.animateClick(500)
        thread_lock.release()

    def toPush(self,cam_name,camid):
        if self.openPush.text()=='开启推流':
            self.openPush.setText("关闭推流")
            rtmpUrl = f'rtmp://43.143.245.240/live/stream{camid}?token={self.token}'
            self.watch = monitorEach_main.MonitorEachMainWindowLocal(token='self.token', user_id='0', cam_id='0',
                                                                     cam_name='0')
            self.watch.show()
            self.pushchild = Thread(target=push_frame, kwargs={'rtmpUrl': rtmpUrl, 'token': self.token, 'cam_id': camid,'cam_name': cam_name,'user_id':self.user_id,'watch':self.watch})
            self.push_flag=True
            self.pushchild.daemon = True
            self.pushchild.start()
        else:
            resp=requests.get(f'http://43.143.245.240:8000/streamoff?token={self.token}&cam_id={camid}')
            # print(resp.text)
            self.watch.close()
            self.push_flag=False
            self.openPush.setText("开启推流")

    def toCam(self):
        if self.push_flag==True and self.watch is not None:
            self.watch.show()
        else:
            QMessageBox.warning(self, '错误', '未开启推流，无法查看本地监控')

    def showMonitors(self):
        self.monitorMenu_win=monitorMenu_main.MonitorMenuMainWindow(token=self.token,user_id=self.user_id)
        self.monitorMenu_win.showMaximized()
        # self.close()

    def toEditMonitors(self):
        self.edit_win = edit_main.EditMainWindow(token=self.token,user_id=self.user_id,local_cam_id=self.local_cam_id)
        self.edit_win.my_Signal.connect(self.resetOpenPush)
        self.edit_win.show()
        # self.close()

    def resetOpenPush(self,t):
        if t=='1':
            self.openPush.setText('添加相机')
            self.openPush.clicked.disconnect()
            self.openPush.clicked.connect(self.toAddCam)
            if self.watch is not None:
                self.watch.close()
            self.watch=None
            return None

    def toShareMonitors(self):
        self.share_win = share_main.ShareMainWindow(token=self.token,user_id=self.user_id)
        self.share_win.show()
        # self.close()

    def toReport(self):
        self.report_win=report_main.ReportMainWindow(token=self.token)
        self.report_win.show()
        # self.close()

    def toAddFace(self):
        self.addface_win = addface_main.AddFaceMainWindow(token=self.token,user_id=self.user_id)
        self.addface_win.show()
        # self.close()

    def closeEvent(self, event):
        if not self.monitorMenu_win is None:
            self.monitorMenu_win.close()
        if not self.edit_win is None:
            self.edit_win.close()
        if not self.share_win is None:
            self.share_win.close()
        if not self.report_win is None:
            self.report_win.close()
        if not self.addface_win is None:
            self.addface_win.close()
        if not self.watch is None:
            self.watch.close()

    def toAddCam(self):
        num = 10
        try:
            index_list = []
            for i in range(0, num):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    index_list.append(i)
                    cap.release()
                else:
                    break
        except Exception as e:
            if len(index_list) <= 0:
                QMessageBox.critical(self, '添加失败', '本机不存在摄像头')
                return
        value, ok = QInputDialog.getText(self, "添加摄像头", "请输入摄像头名称", QLineEdit.Normal, None)
        if value is None or value == '':
            return None
        if not value.isalnum():
            QMessageBox.warning(self, '警告', '相机名只由字母和数字组成！')
            return None
        if len(value)>20:
            QMessageBox.warning(self, '警告', '相机名长度为1-20，请重新输入！')
        headers = random.choice(headers_list)
        datasend = {'token': self.token, 'name': value}
        response = requests.post('http://43.143.245.240:8000/camadd/', data=datasend)
        response = json.loads(response.text)
        if response['code']==0:
            QMessageBox.information(self, '添加成功', f'成功添加新摄像头')
            camid=str(response['cam_id'])
            self.local_cam_id=camid
            self.openPush.setText( "开启推流")
            self.openPush.clicked.disconnect()
            self.openPush.clicked.connect(lambda: self.toPush(str(value),self.local_cam_id))
            path = './face_reg/face_data/' + self.user_id + '_' + value
            if not os.path.exists(path):
                os.makedirs(path+'/pre')
                os.makedirs(path+'/image')
            return None
        if response['msg'] == 'cam name exist':
            QMessageBox.critical(self, '添加失败', '摄像头名已存在')
            return None
        elif response['msg'] == 'cam mac exist':
            QMessageBox.critical(self, '添加失败', 'mac已存在')
            return None





if __name__ == "__main__":
    app = QApplication(sys.argv)
    token1='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIxNGY2ZDg3ZTkxYzMiLCJleHAiOjUwNTM0NDAyMTMuMDI1MDkxfQ.DkmBwqqz0YyxfCUa8-rcljrl2O0cKUs8eQd8LCF3qAA'
    myWin = MenuMainWindow(token=token1)
    myWin.show()
    sys.exit(app.exec_())
