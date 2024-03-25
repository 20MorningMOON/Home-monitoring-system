import json
import sys
from face_reg.process import face_name,delete_name
import os
import pandas as pd
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLineEdit,QTableWidgetItem
from addface import Ui_MainWindow#注意这里的UI文件名及其class名，根据自己定义的来
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
from PyQt5.QtCore import QSize
import requests
import os


class AddFaceMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None,token=None,user_id=None):

        super(AddFaceMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.token=token
        self.user_id = user_id
        self.names=[]
        self.imgs = []
        self.setFixedSize(self.width, self.height)
        self.cam_name_id = {}
        self.faceListId = []
        self.camcurrent_name=""
        self.initComboBox()
        self.pushButton.clicked.connect(self.addFace)
        self.pushButton_2.clicked.connect(self.deleteFace)
        self.pushButton_3.clicked.connect(self.fillFaceTable)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/addface.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)

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

    def fillFaceTable(self):
        if self.cameraComboBox.currentText() == '请选择':
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头')
            return None
        self.faceListId = []
        self.camcurrent_name = self.cameraComboBox.currentText()
        self.camcurrent_id = self.cam_name_id[self.camcurrent_name]
        self.label_5.setText(self.camcurrent_name)
        # print(self.camcurrent_name)
        path = './face_reg/face_data/'+ self.user_id + '_' +self.camcurrent_name
        self.names = []
        self.imgs = []
        if os.path.exists(path + '/name.csv'):
            namelist = pd.read_csv(path + '/name.csv', encoding='utf-8')
            for idx, item in namelist.iterrows():
                self.faceListId.append(item['id'])
                self.names.append(item['name'])
                self.imgs.append(item['img_path'])
            self.tableWidget.setRowCount(len(self.names))
            x = 0
            self.tableWidget.setIconSize(QSize(70, 70))
            for n in range(len(self.names)):
                # self.cam_name_id[str(d['name'])] = str(d['id'])
                self.tableWidget.setRowHeight(x, 70)
                self.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(self.names[n]))
                newItem = QTableWidgetItem(QIcon(self.imgs[n]),'1')
                self.tableWidget.setItem(x, 1, newItem)
                x += 1
            # print(self.faceListId)
        else:
            if os.path.exists(path):
                print(1)
            else:
                self.names=[]
                self.imgs=[]
                self.tableWidget.setRowCount(0)
                QMessageBox.information(self, '提示', '该摄像头非本地摄像头，无法查看和录入人脸信息')
    def addFace(self):
        if self.cameraComboBox.currentText() == '请选择':
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头')
            return None
        self.camcurrent_name = self.cameraComboBox.currentText()
        self.camcurrent_id = self.cam_name_id[self.camcurrent_name]
        value, ok = QInputDialog.getText(self, "添加人脸", "请输入人脸名称后上传图片", QLineEdit.Normal, None)
        if value is None or value == '':
            return None
        else:
            path = './face_reg/face_data/'+ self.user_id + '_' +self.camcurrent_name
            bool_=face_name(value,path)
            if bool_:
                QMessageBox.information(self, '添加成功', f'成功添加名为{value}的人脸')
                self.fillFaceTable()
            else:
                QMessageBox.critical(self, '添加失败', '照片中不能没有人脸或存在多个人脸')
    def deleteFace(self):
        if len(self.faceListId) == 0:
            QMessageBox.critical(self, '提示！', '列表为空')
            return None
        if self.cameraComboBox.currentText() == '请选择':
            QMessageBox.critical(self, '请选择！', '请选择一个摄像头')
            return None
        value, ok = QInputDialog.getText(self, "移除人脸", "请输入需要移除人脸的序号", QLineEdit.Normal, None)
        if value is None or value == '':
            return None
        if not value.isdigit():
            QMessageBox.critical(self, '删除失败', '输入序号不合法')
            return None
        path = './face_reg/face_data/'+ self.user_id + '_' +self.camcurrent_name
        value =int(value)
        if (value-1)>=0 and (value-1)<len(self.faceListId):
            Bool_,name=delete_name(path,self.faceListId[value-1])
            if Bool_:
                QMessageBox.information(self, '移除成功', f'成功移除名字为{name}的人脸')
                self.fillFaceTable()
            else:
                QMessageBox.critical(self, '移除失败', '发生错误')
        else:
            QMessageBox.critical(self, '移除失败', '输入序号不合法')
            return None






if __name__ == '__main__':
    app = QApplication(sys.argv)
    token1='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJtYWMiOiIxNGY2ZDg3ZTkxYzMiLCJleHAiOjUwNTM0NDAyMTMuMDI1MDkxfQ.DkmBwqqz0YyxfCUa8-rcljrl2O0cKUs8eQd8LCF3qAA'
    win = AddFaceMainWindow(token=token1)
    win.show()
    sys.exit(app.exec())