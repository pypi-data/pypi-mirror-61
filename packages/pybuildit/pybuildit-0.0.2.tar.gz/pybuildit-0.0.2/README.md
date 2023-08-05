# Buildit

Buildit Actuator を制御する為のPython3用ライブラリ


## Install

### Windows

```
$ pip3 install pybuildit
```

### Ubuntu

```
$ sudo apt-get -y install python3-tk
$ pip3 install pybuildit
```

## Usage

### pybuildit library

* ライブラリについてのドキュメント
    * https://www.smartrobotics.jp/products/buildit/latest/BuilditActuatorユーザーマニュアル.pdf

* 初期化
    * ※ 以下のデバイスファイル名やCOMポート番号は環境に合わせて変更する必要があります
```
>>> from pybuildit import *
>>> buildit = Buildit(port="/dev/ttyXXXX", timeout_ms=3000) #for Linux
>>> buildit = Buildit(port="COMX", timeout_ms=3000) #for Win
>>> deviceId = 1
```


* 現在の位置や速度といった情報の取得

```
>>> (position, velocity, current, referenceValue, temperature, faults) = buildit.query_servo_status(deviceId)
>>> print(state2str(buildit.state()))
```

* 速度制御と位置制御の方法

```
>>> #buildit.clear_fault(deviceId)
>>> buildit.ready(deviceId)
>>> buildit.set_ref_velocity(deviceId, fromRPM(42.5))
>>> buildit.set_ref_position(deviceId, fromDegree(180))
```


### builditctl

builditctl は Buildit の各メソッドをコマンドラインから呼び出す為のツールです。
アクチュエーターの状態を確認する場合は以下のように実行します。

```
$ builditctl query-servo-status -d 1 -p /dev/ttyUSB0
state: STATE_HOLD
pos: -51636
vel: 0
cur: 0
ref: 0
temp: 26
faults: NO_FAULTS
```

速度制御を行う場合は以下のように実行します。

```
$ builditctl ready -d 1 -p /dev/ttyUSB0

$ builditctl set-ref-velocity 2500 -d 1 -p /dev/ttyUSB0 # 指定速度の単位は [rpm/100]
0
```

位置制御を行う場合は以下のように実行します。

```
$ builditctl stop -d 1 -p /dev/ttyUSB0

$ builditctl set-ref-position 2500 -d 1 -p /dev/ttyUSB0 # 指定位置の単位は [360/65536 度]
-39775
```


### builditct-gui

builditctl は Buildit の各メソッドをコマンドラインから呼び出す為のツールです。

```
$ builditctl-gui
```

ポートを選択し、Connectボタンを押した後、各種ボタンを使ってデバイスを操作することが出来ます。





