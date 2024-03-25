import json
import sys
import random

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QInputDialog, QLineEdit
from share import Ui_MainWindow#注意这里的UI文件名及其class名，根据自己定义的来
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
import requests
from headers_list import headers_list

class ShareMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None,token=None,user_id=None):
        super(ShareMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width,self.height)
        self.token = token
        self.user_id = user_id
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        self.cam_name_id={}
        with open("resource/share.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)
        self.camcurrent_name=None
        self.camcurrent_id = None
        self.initCombobox()
        self.queryBtn.clicked.connect(self.query)
        self.removeBtn.clicked.connect(self.remove)

    def initCombobox(self):
        headers = random.choice(headers_list)
        response = requests.get('http://43.143.245.240:8000/camlist?token=' + self.token,headers=headers)
        response = json.loads(response.text)
        self.cam_id.addItem('请选择')
        data = response['data']
        for d in data:
            self.cam_id.addItem(str(d['name']))
            self.cam_name_id[str(d['name'])]=str(d['id'])


    def query(self):
        self.camcurrent_name=self.cam_id.currentText()
        if self.camcurrent_name=='请选择':
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头')
            return None
        self.camcurrent_id=self.cam_name_id[self.camcurrent_name]
        self.label_4.setText(f"当前摄像头：{self.camcurrent_name}")
        headers = random.choice(headers_list)
        datasend={'token':self.token,'cam_id':self.camcurrent_id}
        response = requests.post('http://43.143.245.240:8000/watcherlist/',headers=headers,data=datasend)
        response = json.loads(response.text)
        data = response['data']
        self.watcherList.setRowCount(len(data))
        self.queryUserName=[]
        x=0
        for d in data:
            self.watcherList.setItem(x,0,QtWidgets.QTableWidgetItem(str(d['user__username'])))
            self.queryUserName.append(str(d['user__username']))
            x+=1


    def remove(self):
        user_id=self.user_id_input.text()
        if self.camcurrent_id is None:
            QMessageBox.critical(self, '移除失败', '请先选择摄像头')
        elif user_id not in self.queryUserName :
            QMessageBox.critical(self,'移除失败', '输入用户名并未拥有当前摄像头')
            return None
        else:
            headers = random.choice(headers_list)
            datasend = {'token': self.token, 'cam_id': self.camcurrent_id,'user_name':user_id}
            response = requests.post('http://43.143.245.240:8000/deletewatch/', headers=headers,data=datasend)
            QMessageBox.information(self, '移除成功', f'成功移除用户{user_id}的的摄像头({self.camcurrent_name})')
            self.query()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    token1='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIwMDUwNTZjMDAwMDgiLCJleHAiOjUwNTExMjkxNTYuMDMzMDI1fQ.tbl6oPBLtFl8oIDrl240itESMI3rmbVPRgegzVjoCuI'
    myWin = ShareMainWindow(token=token1)
    myWin.show()
    sys.exit(app.exec_())