# 毎時59分に実行 
# coding: UTF-8

# ライブラリインポート
from datetime import datetime
import os
import pandas as pd

# ファイル名の設定
now = datetime.now()
filename = now.strftime('%Y%m%d')

# csvファイルの読み込み
pd.set_option('display.max_rows',10)
# df_csv = pd.read_csv('/home/pi/programs/data/'+ filename + '.csv', encoding = 'UTF-8', names = ['hour','min','temp','hum','co2'])
df_csv = pd.read_csv('/home/pi/programs/data/20211004.csv', encoding = 'UTF-8', names = ['hour','min','temp','hum','co2'])

# 時間の読み取り
hour_now = now.hour
hour = 0

# 変数の初期化
i = 0
sum_temp = 0
sum_hum = 0
sum_co2 = 0
ave_temp = 0
ave_hum = 0
ave_co2 = 0

# ファイルを開く
if not os.path.exists('/home/pi/programs/average'):
    os.makedirs('/home/pi/programs/average')
# f = open('/home/pi/programs/average/'+filename+'_ave.csv','w')
f = open('/home/pi/programs/average/20211004_ave.csv','w')

# 計算
while True:
    # if hour == hour_now + 1:
    if hour == 23 + 1:
        break
    for row in df_csv.values:
        if row[0] == hour:
            # print(row)
            sum_temp = sum_temp + row[2]
            sum_hum = sum_hum + row[3]
            sum_co2 = sum_co2 + row[4]
            i = i + 1

    ave_temp = sum_temp / i
    ave_hum = sum_hum / i
    ave_co2 = sum_co2 / i

    print(hour, ave_temp, ave_hum, ave_co2)

    # ファイルへの書き出し
    f.write(str(hour)+","+str(ave_temp)+","+str(ave_hum)+","+str(ave_co2)+"\n")

    hour = hour + 1
    i = 0
    sum_temp = 0
    sum_hum = 0
    sum_co2 = 0
    ave_temp = 0
    ave_hum = 0
    ave_co2 = 0

# ファイルを閉じる
f.close()
