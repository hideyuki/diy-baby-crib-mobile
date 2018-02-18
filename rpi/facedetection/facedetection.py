# -*- coding: utf-8 -*-

import cv2
import subprocess
from datetime import datetime

# カメラの画像を撮影してcapture.jpgとして保存する
res = subprocess.call('./capture.sh')

# capture.jpgをOpenCV用に読み込む
img = cv2.imread("./capture.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 顔認識
cascade_path = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(cascade_path)
faces = cascade.detectMultiScale(gray, 1.3, 5)

print faces

#for (x, y, w, h) in faces:
#  cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 5)

# 顔が1つでもあれば、カメラ画像保存ディレクトリ(~/camera)に保存する
if len(faces) > 0:
    d = datetime.now()
    filename = "/home/pi/camera/" + d.strftime("%Y%m%d-%H%M%S") + ".jpg"
    cv2.imwrite(filename, img)
    print("Face detected! filename: " + filename)

