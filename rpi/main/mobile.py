#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
メリーからの音楽再生／停止コマンドをシリアル通信で受信しつつ、
Alexaからのメリー回転メッセージをMQTTで受信するプログラム

【動作させるために必要なこと】
①audioディレクトリに、mp3ファイルをa0.mp3〜a5.mp3の6つ配置する（sound_id_maxを変更すれば曲数を変更可能）
②certディレクトリに、AWS IoTで作成した「このモノの証明書」（certificate.pem.crt）、
  「プライベートキー」（private.pem.key）、「ルートCA」（rootca.pem）を配置する。
③53行目のendpointを自分のAWS IoTのエンドポイント設定に上書きする
"""

import os
import pygame.mixer
import serial
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json


# いま音楽が再生されているかフラグ
is_play = False
# 現在再生している音楽ID
sound_id = 0
# 最大の音楽ID
sound_id_max = 5
#各曲のボリューム (それぞれの平均音量が異なるため)
volume = [1.0, 0.7, 0.2, 0.6, 0.5, 0.4]


# 音楽再生関係の初期化
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

base_path = os.path.dirname(os.path.abspath(__file__))

# 起動音を鳴らす
pygame.mixer.music.load(base_path + "/audio/startup.mp3")
pygame.mixer.music.play()
time.sleep(3)
pygame.mixer.music.stop()


# シリアル通信の初期化
ser = serial.Serial("/dev/ttyACM0", 9600)

# AWS IoTの初期化
endpoint = "xxxxxxxxxxx.iot.us-east-1.amazonaws.com"  # AWS IoTのエンドポイントを指定してください
rootca_path = base_path + "/cert/rootca.pem"
certificate_path = base_path + "/cert/certificate.pem.crt"
privatekey_path = base_path + "/cert/private.pem.key"
client_id = "mobile"
topic = "home/mobile/1"

# MQTTメッセージのコールバック
def custom_callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    payload = json.loads(message.payload)
    power = payload["power"]
    if power == "ON":
        # メリーを回転させる
        ser.write("n")
    else:
        # メリーの回転を止める
        ser.write("f")

# AWSIoTMQTTClientの初期化
awsiot_mqtt_client = AWSIoTMQTTClient(client_id)
awsiot_mqtt_client.configureEndpoint(endpoint, 8883)
awsiot_mqtt_client.configureCredentials(rootca_path, privatekey_path, certificate_path)
awsiot_mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
awsiot_mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
awsiot_mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
awsiot_mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

# AWS IoTに接続してメリーのトピックを購読する
awsiot_mqtt_client.connect()
awsiot_mqtt_client.subscribe(topic, 1, custom_callback)


while True:
    line = ser.readline()
    command = line[0]

    if command == 'p': # play/stop
        # 音楽の再生/ストップを制御
        print("push play/stop")
        if is_play:
            print("stop")
            pygame.mixer.music.stop()
        else:
            print("play")
            pygame.mixer.music.load(base_path + "/audio/a%d.mp3" % sound_id)
            pygame.mixer.music.set_volume(volume[sound_id])
            pygame.mixer.music.play(-1)

        is_play = not is_play

    elif command == 'n': # next
        # 次の音楽を再生する
        print("push next")
        sound_id += 1
        if sound_id > sound_id_max:
            sound_id = 0

        print("sound_id: %d" % sound_id)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(base_path + "/audio/a%d.mp3" % sound_id)
        pygame.mixer.music.set_volume(volume[sound_id])
        pygame.mixer.music.play(-1)

        is_play = True

