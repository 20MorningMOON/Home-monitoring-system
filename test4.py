import json

from locust import HttpLocust, TaskSequence, between, task, seq_task
import random, string


class MyTaskSet(TaskSequence):
    login_header = {}
    del_params = {}
    headers = random.choice(headers_list)
    @seq_task(1)
    def login(self):
        data = {'username': 'user1', 'password': '123456',
                'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
        response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
        print(json.load(response.text))
    # @seq_task(2)
    # def get_customer(self):
    #     to_get = self.client.request(method="post", url="/index.php/crm/customer/index",
    #                                  params={"page": 1, "limit": 15}, headers=self.login_header)
    #     print(to_get.json())
    #
    # @seq_task(3)
    # def add_customer(self):
    #     self.add_params = {"level": "A（重点客户）", "industry": "金融业", "source": "促销活动", "deal_status": "未成交",
    #                        "telephone": "13555555555"}
    #     self.add_params['name'] = ''.join(random.sample(string.ascii_letters + string.digits, 8))  # 随机生成客户名
    #     to_add = self.client.request(method="post", url="/index.php/crm/customer/save", params=self.add_params,
    #                                  headers=self.login_header)
    #     self.del_params["id[0]"] = to_add.json()['data']['customer_id']
    #     print(to_add.json())
    #
    # @seq_task(4)
    # def del_customer(self):
    #     to_del = self.client.request(method="post", url="/index.php/crm/customer/delete", params=self.del_params,
    #                                  headers=self.login_header)
    #     print(to_del.json())
    #
    # @seq_task(5)
    # @task(3)
    # def index(self):
    #     self.client.get("/index.php/admin/system/index")
    #
    # @seq_task(6)
    # def logout(self):
    #     self.client.post("/index.php/admin/base/logout")
    #

class Mytest(HttpLocust):
    task_set = MyTaskSet
    wait_time = between(5.0, 10.0)

