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
import datetime
if __name__ == '__main__':
    headers = random.choice(headers_list)
    #注册
    # data_correct = {'username': 'Testuser'+'1',
    #         'password': '123456',
    #         'email': '12345@qq.com'
    #         }
    # data_error= {'username': 'Testuser'+'_first',
    #         'email': '123@qq'
    #         }
    # response = requests.post(url="http://43.143.245.240:8000/register/", data=data_correct)
    # print(json.loads(response.text))

    #登录
    # data_correct = {'username': 'Testuser1' , 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # data_error = {'username': 'Testuser1_' , 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # data_form_error={ 'password': '1234567',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data_form_error)
    # response = json.loads(response.text)
    # print(response)

    #watchlist
    # data = {'username': 'user1' , 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token=response['token']
    # response = requests.get('http://43.143.245.240:8000/watchlist?token=' + token, headers=headers)
    # response = json.loads(response.text)
    # print(response)

    #camlist
    # data = {'username': 'user1', 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # response = requests.get('http://43.143.245.240:8000/camlist?token=' + token, headers=headers)
    # response = json.loads(response.text)
    # print(response)

    #camadd
    # data = {'username': 'Testuser1', 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # datasend = {'token': token, 'name': 'cam3'}
    # response = requests.post('http://43.143.245.240:8000/camadd/', data=datasend)
    # response = json.loads(response.text)
    # print(response)

    #watchadd1
    # data = {'username': 'Testuser1', 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # datasend = {'token': token}
    # response = requests.post('http://43.143.245.240:8000/watchadd1/', headers=headers, data=datasend)
    # response = json.loads(response.text)
    # print(response)

    #watchadd2
    # data = {'username': 'Testuser2', 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # datasend = {'token':token, 'cam_token': '91338651'}
    # headers = random.choice(headers_list)
    # response = requests.post('http://43.143.245.240:8000/watchadd2/', headers=headers, data=datasend)
    # response = json.loads(response.text)
    # print(response)

    #deletewatch
    # data = {'username': 'Testuser2', 'password': '123456',
    #                 'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # datasend = {'token': token, 'cam_id': 7417, 'user_name': 'Testuser2'}
    # response = requests.post('http://43.143.245.240:8000/deletewatch/', headers=headers, data=datasend)
    # response = json.loads(response.text)
    # print(response)

    # deletecam
    data = {'username': 'Testuser1', 'password': '123456',
            'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    response = json.loads(response.text)
    token = response['token']
    datasend = {'token': token,'cam_id':1}
    response = requests.post('http://43.143.245.240:8000/deletecam/', headers=headers, data=datasend)
    print(json.loads(response.text))

    #getevent
    data = {'username': 'Testuser1', 'password': '123456',
            'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    response = json.loads(response.text)
    token = response['token']
    print(token)
    response = requests.get('http://43.143.245.240:8000/camlist?token=' + token, headers=headers)
    response = json.loads(response.text)
    data = response['data']

    response_error1 = requests.post('http://43.143.245.240:8000/getevent/',
                                     data={'token': token, 'cam_id': 23, 'event_id': '0'})
    event = json.loads(response_error3.text)
    print(event)
    # response_error2 = requests.post('http://43.143.245.240:8000/getevent/',
    #                                 data={ 'cam_id': 22, 'event_id': '0'})
    # response_error3 = requests.post('http://43.143.245.240:8000/getevent/',
    #                                 data={'token': token,'cam_id': 22})
    #                                 #
    #     # response_correct = requests.post('http://43.143.245.240:8000/getevent/',
    #     #                          data={'token': token, 'cam_id': 22, 'event_id': '0'})


    #downloadeventimage
    # data = {'username': 'Testuser1', 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # response = requests.get('http://43.143.245.240:8000/camlist?token=' + token, headers=headers)
    # response = json.loads(response.text)
    # data = response['data']
    # cam_id=str(data[1]['id'])
    #
    # response = requests.post('http://43.143.245.240:8000/getevent/',
    #                          data={'token': token, 'cam_id': cam_id, 'event_id': '0'})
    # event = json.loads(response.text)
    # event_id=85
    # tc1=time.time()
    # response = requests.get(
    #     f'http://43.143.245.240:8000/downloadeventimage?token={token}&event_id={85}',
    #     stream=True)
    # tc2=time.time()
    # print(tc2-tc1)
    # print(response.headers['Content-Type'] )

    #ifstream
    # data = {'username': 'user1', 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # response=requests.post('http://43.143.245.240:8000/ifstream/', data={ 'cam_id': 24})
    # response = json.loads(response.text)
    # print(response)

    #streamoff
    # data = {'username': 'user1', 'password': '123456',
    #         'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    # response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    # response = json.loads(response.text)
    # token = response['token']
    # print(token)
    # response=requests.get(f'http://43.143.245.240:8000/streamoff?token={token}&cam_id={7415}')
    # response = json.loads(response.text)
    # print(response)

    #reportevent
    data = {'username': 'Testuser1', 'password': '123456',
            'mac': '00ffe6b35ad8&0c7a155f830a&0e7a155f8309&005056c00001&005056c00008&0c7a155f8309'}
    response = requests.post(url="http://43.143.245.240:8000/login/", headers=headers, data=data)
    response = json.loads(response.text)
    token = response['token']
    print(token)
    tc1 = time.time()
    file = {'image': ('img.jpg', open("resource/default.jpg", 'rb'), 'image/jpg')}
    event = requests.post('http://43.143.245.240:8000/reportevent/',
                          data={'token': token, 'cam_id': 1, 'detail': 'smoke',
                                'time': datetime.datetime.now(),
                                'type': '1'}, files={'image': ('img.jpg', open("resource/default.jpg", 'rb'), 'image/jpg')})
    tc2=time.time()
    print(tc2-tc1)
    response = json.loads(event.text)
    print(response)
