import requests
import ssl
import os, base64
import urllib
import cv2
import json
from PIL import Image


# 调用摄像头拍摄照片
def get_face_img():
        saveDir = './photo/'
        if os.path.exists(saveDir):
            file = os.listdir(saveDir) 
            print(file) 
            path = './photo/'+file[0]
            os.remove(path)
            os.rmdir(saveDir)
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

        count = 1  # 图片计数索引
        cap = cv2.VideoCapture(0)
        width, height, w = 640, 480, 360
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        crop_w_start = (width - w) // 2
        crop_h_start = (height - w) // 2
        while True:
            ret, frame = cap.read()  # 获取相框
            frame = frame[crop_h_start:crop_h_start + w, crop_w_start:crop_w_start + w]  # 展示相框
            frame = cv2.flip(frame, 1, dst=None)  # 前置摄像头获取的画面是非镜面的，即左手会出现在画面的右侧，此处使用flip进行水平镜像处理
            cv2.imshow("capture", frame)
            action = cv2.waitKey(1) & 0xFF
            if action == ord('c'):
                saveDir = raw_input(u"请输入新的存储目录：")
                if not os.path.exists(saveDir):
                    os.makedirs(saveDir)
            elif action == ord('p'): 
                cv2.imwrite("%s/%d.jpg" % (saveDir, count), cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA))
                print(u"%s: %d 张图片" % (saveDir, count))
                break
            if action == ord('q'):
                break
        cap.release()  # 释放摄像头
        cv2.destroyAllWindows()  # 丢弃窗口

# 对图片进行编码
def base64_img_urlencode():
    saveDir = './photo/'
    file = os.listdir(saveDir) 
    print(file) 
    path = './photo/'+file[0]
    with open(path, "rb") as f:  # 转为二进制格式
        base64_data = base64.b64encode(f.read())  # 使用base64进行加密
    url_encode_data = urllib.parse.quote(base64_data, safe='/', encoding=None, errors=None)
    return base64_data,url_encode_data


 # 人脸搜索的接口，在人脸库中搜索人脸
def search_face(image):
    image = image
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=24.4ca2f418c892a992ad313b20cb36194d.2592000.1564465193.282335-16676879'
    headers = {
        'Content-Type':'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    data = {
        'image':image,
        'image_type':'BASE64',
        'group_id_list':'jiang',
        'quality_control':'NORMAL',
        'liveness_control':'HIGH'
    }
    # data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data).text
    print('respones',response)


if __name__ == '__main__':
    get_face_img()
    base64_data,url_encode_data = base64_img_urlencode()
    base64_data = str(base64_data)[2:-1]
    search_face(base64_data)
