import json
import sys
import random
from psutil import net_if_addrs

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from login import Ui_Form
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
import requests
import register_main
import menu_main
from headers_list import headers_list

class LoginMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(LoginMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width,self.height)
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.toRegister)
        self.setWindowIcon(QIcon("resource/监控(title).png"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('resource/bg.png')))
        self.setPalette(self.palette)
        with open("resource/logreg.qss") as f:
            qss = f.read()
            self.setStyleSheet(qss)

    def login(self):
        if self.userID.text() == "":
            QMessageBox.warning(self, '警告', '帐号不能为空，请输入！')
            return None
        if self.password.text() == "":
            QMessageBox.warning(self, '警告', '密码不能为空，请输入！')
            return None
        if not self.userID.text().isalnum():
            QMessageBox.warning(self, '警告', '帐号只由字母或数字组成！')
            self.userID.clear()
            self.password.clear()
            return None
        if not self.password.text().isalnum():
            QMessageBox.warning(self, '警告', '密码只由字母或数字组成！')
            self.userID.clear()
            self.password.clear()
            return None
        if len(self.userID.text())<4 or len(self.userID.text())>16:
            QMessageBox.warning(self, '警告', '帐号长度限制为4-16，请确认后重新输入！')
            self.userID.clear()
            self.password.clear()
            return None
        if len(self.password.text())<6 or len(self.password.text())>16:
            QMessageBox.warning(self, '警告', '密码长度限制为6-16，请确认后重新输入！')
            self.userID.clear()
            self.password.clear()
            return None
        mac =''
        for k, v in net_if_addrs().items():
            for item in v:
                address = item[1]
                if '-' in address and len(address) == 17:
                    address = address.replace('-', '').lower()
                    mac=mac+address+'&'
        mac=mac[:-1]
        headers = random.choice(headers_list)
        data={'username':self.userID.text(),'password':self.password.text(),'mac':mac}
        try:
            response=requests.post(url="http://43.143.245.240:8000/login/",headers=headers,data=data)
            response = json.loads(response.text)
            if response['code']==0:
                QMessageBox.information(self, '登录成功', '点击进入下一步')
                # print(response['token'])
                token=response['token']
                print(mac)
                self.menu_win=menu_main.MenuMainWindow(token=token,user_id=self.userID.text())
                self.menu_win.show()
                self.close()
            else:
                QMessageBox.critical(self, '登录失败', '帐号或密码错误，请重新输入')
                self.userID.clear()
                self.password.clear()
                return None
        except Exception as e:
            QMessageBox.critical(self, '登录超时', '请检查网络连接')
            return None

    def toRegister(self):
        self.reg_win = register_main.RegisterMainWindow()
        self.reg_win.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = LoginMainWindow()
    myWin.show()
    sys.exit(app.exec_())