# 毎時59分に実行 
# coding: UTF-8

# 作成するデータの指定
dataname = '20211005'

# ライブラリインポート
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# csvファイルのセットアップ
now = datetime.now()
filename = now.strftime('%Y%m%d')

pd.set_option('display.max_rows',10)
# df_csv = pd.read_csv('/home/pi/programs/average/'+filename+'_ave.csv', encoding = 'UTF-8', names = ['hour','temp_ave','hum_ave','co2_ave'])
df_csv = pd.read_csv('/home/pi/programs/average/'+ dataname +'_ave.csv', encoding = 'UTF-8', names = ['hour','temp_ave','hum_ave','co2_ave'])

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
ax1.plot(x, y1,color = "#FF9933", label = "Temperature", marker='.', markersize=10)
ax2.plot(x, y2,color = "#457Fd3", label = "Humidity", marker='.', markersize=10)

# グラフタイトル・ラベルの設定

# ax1.set_title("Average of Temperature & Humidity")
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature [c]", color = "#FF9933")
ax2.set_ylabel("Humidity [%]", color = "#457Fd3")
fig1.subplots_adjust(bottom = 0.18)
fig1.subplots_adjust(right = 0.86)

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
# plt.savefig('/home/pi/programs/html/image1.png')
plt.savefig('/home/pi/programs/graph/'+ dataname +'_1.png')

# graph2の設定
fig2 = plt.figure(figsize=(7.5, 4.5))
ax3 = fig2.subplots()
ax3.bar(x, y3,color = "#25A31D", label = "Temperature")

# グラフタイトル・ラベルの設定

# ax3.set_title("Average of CO2")
ax3.set_xlabel("Time")
ax3.set_ylabel("Amount of CO2 [ppm]")
fig2.subplots_adjust(bottom = 0.18)
fig2.subplots_adjust(left = 0.1)

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
# plt.savefig('/home/pi/programs/html/image2.png')
plt.savefig('/home/pi/programs/graph/'+ dataname +'_2.png')