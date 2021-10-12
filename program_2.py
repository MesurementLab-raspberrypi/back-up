# 毎時59分に実行 
# coding: UTF-8

# ライブラリインポート
from datetime import datetime
import os
from numpy.core.fromnumeric import size
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ファイル名の設定
now = datetime.now()
filename = now.strftime('%Y%m%d')

# csvファイルの読み込み
pd.set_option('display.max_rows',10)
df_csv = pd.read_csv('/home/pi/programs/data/'+ filename + '.csv', encoding = 'UTF-8', names = ['hour','min','temp','hum','co2'])

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
f = open('/home/pi/programs/average/'+filename+'_ave.csv','w')

# 計算
while True:
        if hour == hour_now + 1:
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
# グラフの出力
# ローカルファイルへの出力
if not os.path.exists('/home/pi/programs/graph'):
        os.makedirs('/home/pi/programs/graph')

# csvファイルのセットアップ
pd.set_option('display.max_rows',10)
df_csv = pd.read_csv('/home/pi/programs/average/'+filename+'_ave.csv', encoding = 'UTF-8', names = ['hour','temp_ave','hum_ave','co2_ave'])

# 各列をそれぞれ変数に代入
first = df_csv.hour
second = df_csv.temp_ave
third = df_csv.hum_ave
fourth = df_csv.co2_ave

# 出力する列の指定
x = first
y1 = second
y2 = third
y3 = fourth

# graph1の設定
fig1 = plt.figure(figsize=(7.5, 4.5))
ax1 = fig1.subplots()
ax2 = ax1.twinx()
ax1.plot(x, y1,color = "#FF6600", label = "Temperature", marker='.', markersize=10)
ax2.plot(x, y2,color = "#457Fd3", label = "Humidity", marker='.', markersize=10)

# グラフタイトル・ラベルの設定

ax1.set_title("Average of Temperature & Humidity", size = 20)
ax1.set_xlabel("Time",  size = 15)
ax1.set_ylabel("[c]",  size = 15)
ax2.set_ylabel("[%]",  size = 15)
fig1.subplots_adjust(bottom =0.18)
# fig1.subplots_adjust(right = 0.86)

# メモリの最大・最小値の設定
ax1.set_xlim(-0.5,24.5)
ax1.set_ylim(0,50)
ax2.set_ylim(0,100)

# メモリ間隔の設定
ax1.set_xticks(np.arange(0, 25, step = 2))

#凡例
# h1, l1 = ax1.get_legend_handles_labels()
# h2, l2 = ax2.get_legend_handles_labels()
# ax1.legend(h1+h2, l1+l2 ,loc='upper left')

#補助メモリの作成
ax1.grid(which = "major", axis = "y", color = "grey", alpha = 0.8,
        linestyle = "--", linewidth = 1)
ax1.grid(which = "major", axis = "x", color = "grey", alpha = 0.8,
        linestyle = "--", linewidth = 1)

# グラフのプロット
plt.savefig('/var/www/html/image1.png')
plt.savefig('/home/pi/programs/graph/'+ filename +'_1.png')
plt.savefig('/home/pi/programs/html/image1.png')

# graph2の設定
fig2 = plt.figure(figsize=(7.5, 4.5))
ax3 = fig2.subplots()
ax3.bar(x, y3,color = "#25A31D", label = "Temperature")

# グラフタイトル・ラベルの設定

ax3.set_title("Average of CO2", size = 20)
ax3.set_xlabel("Time", size = 15)
ax3.set_ylabel("[ppm]", size = 15)
fig2.subplots_adjust(bottom = 0.18)
# fig2.subplots_adjust(right = 0.88)

# メモリの最大・最小値の設定
ax3.set_xlim(-0.5,24.5)
ax3.set_ylim(0,5000)

# メモリ間隔の設定
ax3.set_xticks(np.arange(0, 25, step = 2))

#補助メモリの作成
ax3.grid(which = "major", axis = "y", color = "grey", alpha = 0.8,
        linestyle = "--", linewidth = 1)
ax3.grid(which = "major", axis = "x", color = "grey", alpha = 0.8,
        linestyle = "--", linewidth = 1)

# グラフのプロット
plt.savefig('/var/www/html/image2.png')
plt.savefig('/home/pi/programs/graph/'+ filename +'_2.png')
plt.savefig('/home/pi/programs/html/image2.png')