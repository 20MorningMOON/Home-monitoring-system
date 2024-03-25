import tensorflow as tf
import face_reg.detect_face as detect_face
import face_reg.facenet as facenet
from face_reg.process import *
with tf.Graph().as_default():
    sess = tf.compat.v1.Session()
    with sess.as_default():
        pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
with tf.Graph().as_default():
    with tf.compat.v1.Session() as sess:
        # 根据模型文件载入模型
        model_facenet = './face_reg/model/model.pb'
        facenet.load_model(model_facenet)
        # 得到输入、输出等张量
        images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
        b1 = []
        name=[]
        box=[]
        time1=0
        frame_rec=cv2.imread('./4.jpg')
        pres, names = get_img_pre_and_name('./face_reg/face_data/' + 'user2' + '_' + 'camTes2')
        result, dist, name,frame,box=face_verification(name, box, sess, frame_rec, time1, pnet, rnet, onet,
                                                                           images_placeholder,
                                                                           embeddings, phase_train_placeholder, pres, names)
        cv2.imshow('wname', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.destroyWindow(wname)