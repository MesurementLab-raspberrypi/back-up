# coding: UTF-8

# ライブラリインポート
from datetime import datetime
import time
import smbus
import os

# MH Z19 専用ライブラリインポート
import mh_z19

# AM2320 セットアップ
i2c = smbus.SMBus(1)
addr = 0xb8 >> 1 #5c\

# 時刻の取得
dt = datetime.now()
date = dt.strftime('%Y年%m月%d日')
hour = dt.strftime('%H')
min = dt.strftime('%M')
# MH Z19 データ読み取り
co2 = mh_z19.read() #読み込んだデータの代入
        
#  AM2320 データ読み取り
try:
    i2c.read_byte(addr)            
except IOError:
    try:
        i2c.write_i2c_block_data(addr,0x03,[0x00,0x04]) 
        time.sleep(0.003)
        data = i2c.read_i2c_block_data(addr,0x03,6)
    except IOError:
        print("error")
humidity = (data[2] << 8 | data[3])/10.0    #読み込んだデータの代入
temp = (data[4] << 8 | data[5])/10.0        #読み込んだデータの代入            

# csvファイルのセットアップ
now = datetime.now()
filename = now.strftime('%Y%m%d')

# csvファイルへの書き出し
if not os.path.exists('/home/pi/programs/data'):
    os.makedirs('/home/pi/programs/data')
f = open('/home/pi/programs/data/'+filename+'.csv','a')
f.write(hour+","+min+","+str(temp)+","+str(humidity)+","+str(co2)+"\n")
f.close()    

# データの書き出し
print (date, hour,":", min, temp,"C ",humidity,"%",co2,"ppm")