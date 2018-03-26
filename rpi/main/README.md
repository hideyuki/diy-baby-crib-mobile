# Raspberry Piの初期設定
ホームディレクトリで以下のコマンドを実行

```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python-opencv python-pip
sudo apt-get install git

git clone ssh://git@github.com/hideyuki/diy-baby-crib-mobile.git

cd rpi/main
sudo apt-get install libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
sudo pip install -r requirements.txt
```
