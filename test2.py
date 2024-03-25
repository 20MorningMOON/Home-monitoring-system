import time
import json
import random
from urllib.error import URLError
from urllib import request
import http.client
import requests
import gevent
from gevent import monkey
from headers_list import headers_list
# 补丁
monkey.patch_all()

def run1(token,i):

    """三种模拟请求"""

    # num = random.randint(100, 999)
    #
    # data = make_data(num)
    headers = random.choice(headers_list)
    try:

        # s1:request请求获取服务器数据
        # response = requests.get('http://43.143.245.240:8000/camlist?token=' + token, headers=headers)
        # response = json.loads(response.text)
        # data = response['data']
        # print(data)

        #s2:request请求修改服务器数据
        # datasend = {'token': token, 'cam_token': str('19155902')}
        # response = requests.post('http://43.143.245.240:8000/watchadd2/', headers=headers, data=datasend)
        # response = json.loads(response.text)
        # print('ok:'+str(response['code']))
        # datasend = {'token': token, 'cam_id': '22', 'user_name': 'Testuser1'}
        # response = requests.post('http://43.143.245.240:8000/deletewatch/', headers=headers, data=datasend)
        # print(json.loads(response.text)['code'])

        #s3:request请求注册账号
        # data = {'username': 'Testuser'+str(k),
        #         'password': '123456',
        #         'email': '123@qq.com'+str(k)
        #         }
        # response = requests.post(url="http://43.143.245.240:8000/register/", data=data)
        # print(json.loads(response.text)['msg'])

        #s4:request请求添加摄像头
        # datasend = {'token': token, 'name': 'cam'+str(k)}
        # response = requests.post('http://43.143.245.240:8000/camadd/', data=datasend)
        # response = json.loads(response.text)
        # print(response['code'],k)
        # print(str(response['cam_id']))
        #s5:request请求删除摄像头
        begin_time = time.time()
        response = requests.get(
            f'http://43.143.245.240:8000/downloadeventimage?token={token}&event_id={1}',
            stream=True)
        end_time = time.time()
        print(i,end_time-begin_time)
        print(json.loads(response.text))
    except URLError as e:

        print('请求', e)

    except Exception as e:

        print('请求错误：', e)

# def call_gevent(count):
#     headers = random.choice(headers_list)
#     data1 = {'username': 'user1', 'password': '123456',
#             'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
#     data2 = {'username': 'user2', 'password': '123456',
#             'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
#     data3 = {'username': 'Testuser1', 'password': '123456',
#              'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
#     response1 = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data1)
#     response2 = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data2)
#     response3 = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data3)
#     token=[]
#     response1 = json.loads(response1.text)
#     response2 = json.loads(response2.text)
#     response3 = json.loads(response3.text)
#     # token.append(response1['token'])
#     token.append(response3['token'])
#     # token.append(response2['token'])
#     """调用gevent 模拟高并发"""
#     run_gevent_list = []
#     for i in range(count):
#         print('--------------%d--Test-------------' % i)
#         g1 = gevent.spawn(run1, token)
#         run_gevent_list.append(g1)
#     begin_time = time.time()
#     gevent.joinall(run_gevent_list)
#     print(1)
#     end = time.time()
# def call_gevent(count):
#     headers = random.choice(headers_list)
#     """调用gevent 模拟高并发"""
#     run_gevent_list = []
#     token=[]
#     for i in range(count):
#         data = {'username': 'Testuser' + str(i+4301),
#                 'password': '123456',
#                 'email': '123@qq.com' + str(i+4301)
#                 }
#         response = requests.post(url="http://43.143.245.240:8000/register/", data=data)
#         data = {'username': 'Testuser' + str(i + 4301), 'password': '123456',
#                 'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
#         response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
#         response = json.loads(response.text)
#         print(i+4301)
#         token.append(response['token'])
#     for i in range(count):
#         g1=gevent.spawn(run1,token[i],i+4301)
#         run_gevent_list.append(g1)
#         print('--------------%d--Test-------------' % i)
#     print(run_gevent_list)
#     begin_time = time.time()
#     gevent.joinall(run_gevent_list)
#     print(1)
#     end = time.time()
#     print('单次测试时间(平均)s:', (end - begin_time) / count)
#     print('累计测试时间 s:', end - begin_time)

def call_gevent(count):
    headers = random.choice(headers_list)
    """调用gevent 模拟高并发"""
    run_gevent_list = []
    token=[]
    cam_Id=[]
    for i in range(count):
        data = {'username': 'Testuser' + str(i + 1), 'password': '123456',
                'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
        response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
        response = json.loads(response.text)
        print(i+1)
        token.append(response['token'])
    for i in range(count):
        g1=gevent.spawn(run1,token[i],i+1)
        run_gevent_list.append(g1)
        print('--------------%d--Test-------------' % i)
    print(run_gevent_list)
    begin_time = time.time()
    gevent.joinall(run_gevent_list)
    print(1)
    end = time.time()
    print('单次测试时间(平均)s:', (end - begin_time) / count)
    print('累计测试时间 s:', end - begin_time)
if __name__ == '__main__':
    headers = random.choice(headers_list)
    # 10万并发请求
    call_gevent(1000)