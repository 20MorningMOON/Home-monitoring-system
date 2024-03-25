import json
import random
import shutil
import sys
import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLineEdit
from edit import Ui_MainWindow#注意这里的UI文件名及其class名，根据自己定义的来
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
import requests
from headers_list import headers_list


class EditMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None,token=None,user_id=None,local_cam_id=None):
        super(EditMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.token=token
        self.user_id = user_id
        self.local_cam_id=local_cam_id
        self.setFixedSize(self.width, self.height)
        # self.back.clicked.connect(self.backMenu)
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/edit.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)
        self.add1.clicked.connect(self.addWatch)
        self.delete1.clicked.connect(self.deleteWatch)
        self.delete2.clicked.connect(self.deleteCam)
        self.share.clicked.connect(self.shareCam)
        if self.token is not None:
            self.fillCamTable(self.token)
            self.fillWatchTable(self.token)

    my_Signal=QtCore.pyqtSignal(str)

    def fillCamTable(self,token):
        headers = random.choice(headers_list)
        response = requests.get('http://43.143.245.240:8000/camlist?token=' + token,headers=headers)
        # print(response.text)
        response = json.loads(response.text)
        data = response['data']
        if (len(data)==0):
            self.camList.setRowCount(0)
            return None
        self.camList.setRowCount(len(data))
        self.camListId=[]
        self.camListName=[]
        x = 0
        for d in data:
            self.camList.setItem(x, 0, QtWidgets.QTableWidgetItem(str(d['name'])))
            self.camListId.append(str(d['id']))
            self.camListName.append(str(d['name']))
            x += 1

    def fillWatchTable(self,token):
        headers = random.choice(headers_list)
        response = requests.get('http://43.143.245.240:8000/watchlist?token=' + token,headers=headers)
        response = json.loads(response.text)
        data = response['data']
        if (len(data)==0):
            self.watchList.setRowCount(0)
            return None
        self.watchList.setRowCount(len(data))
        self.watchListId=[]
        x = 0
        for d in data:
            self.watchList.setItem(x, 0, QtWidgets.QTableWidgetItem(str(d['cam__name'])))
            self.watchListId.append(str(d['cam__id']))
            x += 1
    def addWatch(self):
        value, ok = QInputDialog.getText(self, "添加观看摄像头", "请输入分享密钥", QLineEdit.Normal, None)
        if value is None or value=='':
            return None
        if not value.isdigit():
            QMessageBox.warning(self, '错误', '分享码只由8位数字组成！')
            return None
        if len(value)!=8:
            QMessageBox.warning(self, '错误', '分享码只由8位数字组成！')
            return None
        datasend = {'token': self.token, 'cam_token': str(value)}
        headers = random.choice(headers_list)
        response = requests.post('http://43.143.245.240:8000/watchadd2/',headers=headers, data=datasend)
        response = json.loads(response.text)
        if response['code']==0:
            QMessageBox.information(self, '添加成功', '成功添加新摄像头')
            self.fillWatchTable(self.token)
            return None
        elif response['code']==500:
            QMessageBox.critical(self, '添加失败', '分享码错误')
            return None
        if response['msg']=='no cam':
            QMessageBox.critical(self, '添加失败', 'cam可能已经被删除')
            return None
        elif response['msg']=='own cam':
            QMessageBox.critical(self, '添加失败', '不能添加自己的摄像头')
            return None
        elif response['msg']=='cam exist':
            QMessageBox.critical(self, '添加失败', '已经添加过该摄像头')
            return None


    def deleteWatch(self):
        value, ok = QInputDialog.getText(self, "移除摄像头", "请输入需要移除摄像头的序号", QLineEdit.Normal, None)
        if value is None or value == '':
            return None
        if not value.isdigit():
            QMessageBox.critical(self, '删除失败', '输入序号不合法')
            return None
        value =int(value)
        if (value-1)>=0 and (value-1)<len(self.watchListId):
            headers = random.choice(headers_list)
            datasend = {'token': self.token, 'cam_id': self.watchListId[value-1],'user_name':self.user_id}
            response = requests.post('http://43.143.245.240:8000/deletewatch/', headers=headers,data=datasend)
            if json.loads(response.text)['code']==0:
                QMessageBox.information(self, '移除成功', f'成功移除序号为{value}的摄像头')
                if self.token is not None:
                    self.fillWatchTable(self.token)
            else:
                QMessageBox.critical(self, '移除失败', '发生错误')
        else:
            QMessageBox.critical(self, '移除失败', '输入序号不合法')
            return None


    def deleteCam(self):
        value, ok = QInputDialog.getText(self, "删除摄像头", "请输入需要删除摄像头的序号", QLineEdit.Normal, None)
        if value is None or value=='':
            return None
        if not value.isdigit():
            QMessageBox.critical(self, '删除失败', '输入序号不合法')
            return None
        value = int(value)
        if (value-1)>=0 and (value-1)<len(self.camListId):
            ifstream = json.loads(
                (requests.post('http://43.143.245.240:8000/ifstream/',
                               data={'token': self.token, 'cam_id': int(self.camListId[value-1])}).text))[
                'status']
            if not ifstream == 'no streaming':
                result=QMessageBox.question(self, '提示', '当前摄像头正在工作，是否强制断开连接并删除', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  #默认关闭界面选择No
                if result == QMessageBox.No:
                    return None
            headers = random.choice(headers_list)
            datasend={'token':self.token,'cam_id':int(self.camListId[value-1])}
            if self.local_cam_id is not None and self.camListId[value-1]==self.local_cam_id:
                self.my_Signal.emit('1')
            response = requests.post('http://43.143.245.240:8000/deletecam/', headers=headers,data=datasend)
            QMessageBox.information(self, '删除成功', f'成功删除序号为{value}的摄像头')
            path = './face_reg/face_data/' + self.user_id + '_' + self.camListName[value-1]
            if os.path.exists(path):
                shutil.rmtree(path)
            if self.token is not None:
                self.fillCamTable(self.token)
        else:
            QMessageBox.critical(self,'删除失败','输入序号不合法')
            return None


    def shareCam(self):
        value, ok = QInputDialog.getText(self, "分享摄像头", "请输入需要分享摄像头的序号", QLineEdit.Normal, None)
        if value is None or value=='':
            return None
        if not value.isdigit():
            QMessageBox.critical(self, '分享失败', '输入序号不合法')
            return None
        value = int(value)
        if (value-1)>=0 and (value-1)<len(self.camListId):
            headers = random.choice(headers_list)
            datasend = {'token': self.token, 'cam_id': int(self.camListId[value-1])}
            response = requests.post('http://43.143.245.240:8000/watchadd1/', headers=headers,data=datasend)
            response = json.loads(response.text)
            response=response['cam_token']
            QMessageBox.information(self, '分享成功', f'分享密钥为{response}')
        else:
            QMessageBox.critical(self, '分享失败', '输入序号不合法')
            return None



if __name__ == '__main__':
    app = QApplication(sys.argv)
    token1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIwMDUwNTZjMDAwMDgiLCJleHAiOjUwNTExMjkxNTYuMDMzMDI1fQ.tbl6oPBLtFl8oIDrl240itESMI3rmbVPRgegzVjoCuI'
    win = EditMainWindow(token=None)
    win.show()
    sys.exit(app.exec())