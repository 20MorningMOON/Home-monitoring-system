import copy
import time

import cv2
import subprocess as sp
from MulThreadUtil import YOLOV5,nms,xywh2xyxy,filter_box,draw
import requests
import datetime
import face_reg.detect_face as detect_face
import face_reg.facenet as facenet
from face_reg.process import *
import json
import threading
import monitorEach_main

thread_lock = threading.Lock()
import tensorflow as tf
import threading
global firecount
global smokecount
global strangerscount
global frame_rec
frame_rec=None
global fire_box
fire_box=None
global face_box
face_box=None
global face_name
face_name=None
global fire_count
fire_count=0
global face_count
face_count=0
def recognize_fire_and_face(token,cam_id,cam_name,user_id):
    model = YOLOV5("resource/best.onnx")
    model_facenet = './face_reg/model/model.pb'
    global firecount
    global smokecount
    global strangerscount
    firecount = 0
    smokecount = 0
    strangerscount = 0
    timer = threading.Timer(15, emptycount)
    timer.start()

    tp1 = 0
    tp2 = 0
    tp3 = 0
    tc1 = 0
    tc2 = 0
    tc3 = 0
    with tf.Graph().as_default():
        sess = tf.compat.v1.Session()
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
    with tf.Graph().as_default():
        with tf.compat.v1.Session() as sess:
            # 根据模型文件载入模型
            facenet.load_model(model_facenet)
            # 得到输入、输出等张量
            images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
            b1 = []
            pres, names = get_img_pre_and_name('./face_reg/face_data/' + user_id+'_' +cam_name)
            # print(names)
            time1 = 0
            name = []
            box = []
            while True:
                thread_lock.acquire()
                global frame_rec
                if not frame_rec is None:
                    if not names is None:
                        result, dist, name, frame, box = face_verification(name, box, sess, frame_rec, time1, pnet, rnet, onet,
                                                                           images_placeholder,
                                                                           embeddings, phase_train_placeholder, pres, names)
                        global face_box
                        face_box=copy.deepcopy(box)
                        global face_name
                        face_name=copy.deepcopy(name)
                    if time1%5==0:
                        output, or_img = model.inference(frame_rec)
                        outbox = filter_box(output, 0.5, 0.7)
                        # if outbox != []:
                        #     print(outbox)
                        global fire_box
                        fire_box=copy.deepcopy(outbox)
                        Class, Score = draw(or_img, outbox)
                        if Class is not None and Class == 'smoke':
                            smokecount += 1
                            if smokecount == 10:
                                tc1 = datetime.datetime.now()
                                smokecount = 0
                                if tp1 == 0 or (tc1 - tp1).seconds >= 10:
                                    cv2.imwrite('resource/default.jpg', or_img)
                                    file = {'image': ('img.jpg', open("resource/default.jpg", 'rb'), 'image/jpg')}
                                    event = requests.post('http://43.143.245.240:8000/reportevent/',
                                                          data={'token': token, 'cam_id': cam_id, 'detail': 'smoke',
                                                                'time': tc1,
                                                                'type': '1'}, files=file)
                                    event = json.loads(event.text)['event_id']
                                    tp1 = tc1

                        elif Class is not None and Class == 'fire':
                            firecount += 1
                            if firecount == 10:
                                tc2 = datetime.datetime.now()
                                firecount = 0
                                if tp2 == 0 or (tc2 - tp2).seconds >= 10:
                                    cv2.imwrite('resource/default.jpg', or_img)
                                    file = {'image': ('img.jpg', open("resource/default.jpg", 'rb'), 'image/jpg')}
                                    event = requests.post('http://43.143.245.240:8000/reportevent/',
                                                          data={'token': token, 'cam_id': cam_id, 'detail': 'fire',
                                                                'time': tc2,
                                                                'type': '1'}, files=file)
                                    event = json.loads(event.text)['event_id']
                                    tp2 = tc2

                    for i in name:
                        if i == '陌生人':
                            strangerscount += 1
                    if '陌生人' in name:
                        if strangerscount == 30:
                            tc3 = datetime.datetime.now()
                            strangerscount = 0
                            if tp3 == 0 or (tc3 - tp3).seconds >= 10:
                                cv2.imwrite('resource/strangers.jpg', frame)
                                file = {'image': ('img.jpg', open("resource/strangers.jpg", 'rb'), 'image/jpg')}
                                event = requests.post('http://43.143.245.240:8000/reportevent/',
                                                      data={'token': token, 'cam_id': cam_id, 'detail': 'strangers',
                                                            'time': tc3,
                                                            'type': '1'}, files=file)
                                event = json.loads(event.text)['event_id']
                                tp3 = tc3
                    time1 += 1
                thread_lock.release()


def push_frame(rtmpUrl,token,cam_id,cam_name,user_id,watch):
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ffmpeg command
    command = ['ffmpeg',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', "{}x{}".format(width, height),
               '-re',
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               '-g', '5',
               '-b', '700000',
               rtmpUrl]

    # 设置管道
    p = sp.Popen(command, stdin=sp.PIPE)
    recognize = threading.Thread(target=recognize_fire_and_face, kwargs={'token': token, 'cam_id': cam_id, 'cam_name': cam_name,'user_id': user_id})
    recognize.start()


    while True:
        ret, frame = cap.read()
        p.stdin.write(frame.tostring())
        # thread_lock.acquire()
        global frame_rec
        frame_rec = copy.deepcopy(frame)
        global fire_box
        if not fire_box is None:
            draw(frame,fire_box)
            global fire_count
            fire_count+=1
            if firecount==10:
                fire_count=0
                fire_box=None
        global face_box
        global face_name
        if not face_box is None:
            if (len(face_box)) >= 1 and len(face_box) == len(face_name):
                i = 0
                for x1, y1, x2, y2, h in face_box:
                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)
                    # print(x1, x2, y1, y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color=[255, 255, 255], thickness=2)
                    if len(face_name) != 0:
                        frame = img_ksh(frame, face_name[i], x1, y1)
                        i += 1
                global face_count
                face_count += 1
                if face_count == 10:
                    face_count = 0
                    face_box = None
        watch.frame=copy.deepcopy(frame)

        # thread_lock.release()


def emptycount():
    while True:
        global firecount
        firecount=0
        global smokecount
        smokecount=0
        global strangerscount
        strangerscount = 0
        time.sleep(10)
