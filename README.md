# Alexaにも対応!!自作の赤ちゃんメリー

![](https://github.com/hideyuki/diy-baby-crib-mobile/blob/master/images/mobile.jpg?raw=true)


## 機能

### メリー回転機能
よくある、ベットサイドでくるくる回るメリーの標準機能です。

### 音楽再生機能
Raspberry Pi の中に置かれている複数のmp3ファイルを再生可能です。

### 赤ちゃんの顔認識による自動カメラ撮影機能
赤ちゃんがベットの上にいる時に、自動でカメラ撮影を行います。
この画像を見返せば、赤ちゃんの成長を実感することができるでしょう。

### Alexa対応
Echoに「アレクサ、メリーをつけて」と言えばメリーが回りだします。
（メリー自体に回転ON/OFFボタンがあるので、あまり意味がない可能性があります）



## ディレクトリ構成

### 3d-models
- 3Dプリント用のデータが格納されています。
- 3Dデータはすべて Autodesk Inventor Professional 2014 で作成されています。
- ipt ディレクトリに Inventor ファイルが、stl ディレクトリに STL ファイルが格納されています。
  - 一般的な3Dプリンタでは STL ファイルを印刷するようにしてください。

### arduino
- Arduino の mobile プロジェクトが格納されています。
- Arduino UNO に Arduino IDE を使って書き込んでください。

### aws-alexa-iot
- AWSにお手軽にLambdaをデプロイできる Serverless のプロジェクトが格納されています。
- Alexa は別途 Alexa Developer でスマートホームスキルを定義する必要があります。
- Lambda の関数は Node.js (6.10) で作成しています。

### rpi
- Raspberry Piに配置するファイルが格納されています。
- facedetection
  - 顔認識ができたらカメラ画像を保存するPythonスクリプトです。
- main
  - Arduinoからの音楽再生/メリー回転コマンドの受信（シリアル通信）
  - AWS IoTからのメリー回転メッセージの受信およびArudinoへのメリー回転コマンドの送信（AWS IoTのMQTT)
- settngs
  - crontab: facedetectionを毎時0分に実行するための設定。crontab -eで設定してください。
  - rc.local: Ubuntu起動時に自動でmainのスクリプトが動作するように、/etc/rc.localにこのファイルを配置してください。

