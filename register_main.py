import json
import sys

from PyQt5.QtCore import QFile, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from register import Ui_Form#注意这里的UI文件名及其class名，根据自己定义的来
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
import requests
import login_main
import re

class RegisterMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(RegisterMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(480,531)
        self.registerBtn.clicked.connect(self.register)
        self.backBtn.clicked.connect(self.back)
        # self.getVerifyBtn.clicked.connect(self.getVerify)
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/logreg.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)

    def register(self):
        if self.userID.text() == "":
            QMessageBox.warning(self, '警告', '帐号不能为空，请输入！')
            return None

        if self.password.text() == "":
            QMessageBox.warning(self, '警告', '密码不能为空，请输入！')
            return None

        if not self.userID.text().isalnum():
            QMessageBox.warning(self, '警告', '帐号只由字母或数字组成！')
            return None
        if not self.password.text().isalnum():
            QMessageBox.warning(self, '警告', '密码只由字母或数字组成！')
            return None

        if len(self.userID.text()) < 4 or len(self.userID.text()) > 16:
            QMessageBox.warning(self, '警告', '帐号长度限制为4-16，请确认后重新输入！')
            self.userID.clear()
            self.password.clear()
            return None
        if len(self.password.text()) < 6 or len(self.password.text()) > 16:
            QMessageBox.warning(self, '警告', '密码长度限制为6-16，请确认后重新输入！')
            self.userID.clear()
            self.password.clear()
            return None

        if self.repassword.text() == "":
            QMessageBox.warning(self, '警告', '确认密码不能为空，请输入！')
            return None

        if self.email.text() == "":
            QMessageBox.warning(self, '警告', '邮箱地址不能为空，请输入！')
            return None
        elif self.email.text()!="":
            str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
            if self.email.text()[-3:-1]!='com':
                QMessageBox.warning(self, '警告', '邮箱地址格式错误，请确认后重新输入！')
                self.email.clear()
                return None
            if not re.match(str,self.email.text()):
                QMessageBox.warning(self, '警告', '邮箱地址格式错误，请确认后重新输入！')
                self.email.clear()
                return None

        if self.password.text() != self.repassword.text():
            QMessageBox.warning(self, '警告', '两次密码不同，请重新输入！')
            self.password.clear()
            self.repassword.clear()
            return None

        data = {'username': self.userID.text(),
                'password': self.password.text(),
                'email': self.email.text()
                }
        response = requests.post(url="http://43.143.245.240:8000/register/", data=data)
        if json.loads(response.text)['msg'] == 'success':
            QMessageBox.information(self, '注册成功', '点击\'返回\'去登录吧！')
        else:
            msg=json.loads(response.text)['msg']
            if msg=='user exist':
                QMessageBox.critical(self, '注册失败', '用户名已存在！')
            elif msg=='email existed':
                QMessageBox.critical(self, '注册失败', '该邮箱已注册！')
            elif msg=='form error':
                QMessageBox.critical(self, '注册失败', '提交参数错误！')
            else:
                QMessageBox.critical(self, '注册失败', '未知错误！')
            self.userID.clear()
            self.password.clear()
            self.repassword.clear()
            self.email.clear()
            return None

    def back(self):
        self.login_win=login_main.LoginMainWindow()
        self.login_win.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = RegisterMainWindow()
    myWin.show()
    sys.exit(app.exec_())