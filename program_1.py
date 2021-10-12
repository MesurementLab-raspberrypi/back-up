# coding: UTF-8

# ライブラリインポート
from datetime import datetime
import time
import smbus
import os
import sys

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

# プログラムの動作確認
if temp == None or humidity == None or co2 == None:
    sys.exit

# csvファイルのセットアップ
now = datetime.now()
filename = now.strftime('%Y%m%d')

# csvファイルへの書き出し
if not os.path.exists('/home/pi/programs/data'):
    os.makedirs('/home/pi/programs/data')
# f = open('/home/pi/programs/data/'+filename+'.csv','a')
f = open('/home/pi/programs/data/'+filename+'.csv','a')
f.write(hour+","+min+","+str(temp)+","+str(humidity)+","+str(co2)+"\n")
f.close()

# データの書き出し
print (date, hour,":", min, temp,"C ",humidity,"%",co2,"ppm")

# program_2

data1 = temp
data2 = humidity
data3 = co2

# 円グラフの割合計算
rate1 = temp /40 *100
rate2 = humidity /100 *100
rate3 = co2 /5000 *100

# htmlの生成
f = open('/var/www/html/index.html','w')
f.write(
    '    <!DOCTYPE html>\n'
    '<html lang="ja">\n'
    '\n'
    '<head>\n'
    '    <meta charset="UTF-8" />\n'
    '    <title>ラズパイ CO2・温湿度計</title>\n'
    '    <link rel="stylesheet" type="text/css" href="style_pc.css" />\n'
    '    <link rel="stylesheet" type="text/css" href="style_tablet.css" />\n'
    '    <link rel="stylesheet" type="text/css" href="style_phone.css" />\n'
    '    <link rel="stylesheet" type="text/css" href="style.css" />\n'
    '    <meta http-equiv="refresh" content="60">\n'
    '</head>\n'
    '\n'
    '<body>\n'
    '    <main>\n'
    '        <div class="top">\n'
    '            <div class="time">\n'
    '                <div class="row1">\n'
    '                    <h1 id="Clock"></h1>\n'
    '                    <h2 id="Ampm"></h2>\n'
    '                </div>\n'
    '                <div class="row2">\n'
    '                    <h3 id="Calendar"></h3>\n'
    '                </div>\n'
    '            </div>\n'
    '            <div class="co2_box">\n'
    '                <h4 class="co2">CO<sub>2</sub> [ppm]</h4>\n'
    '                <div class="graph_co2"><span><h5 class="co2">' + str(data3) + '</h5></span></div>\n'
    '            </div>   \n'
    '            <div class="temp_box">\n'
    '                <h4 class="temp">Temperature [℃]</h4>\n'
    '                <div class="graph_temp"><span><h5 class="temp">' + str(data1) + '</h5></span></div>\n'
    '            </div>\n'
    '            <div class="hum_box">\n'
    '                <h4 class="humidity">Humidity [%]</h4>\n'
    '                <div class="graph_humidity"><span><h5 class="humidity">' + str(data2) + '</h5></span></div>\n'
    '            </div>\n'
    '        </div>\n'
    '        <div class="bottom">\n'
    '            <img class="image" src="image2.png">\n'
    '            <img class="image" src="image1.png">\n'
    '        </div>\n'
    '\n'
    '        <!-- java script -->\n'
    '        <script>\n'
    '        function set2fig(num) {\n'
    '            var ret;\n'
    '            if( num < 10 ) { ret = "0" + num; }\n'
    '            else { ret = num; }\n'
    '            return ret;\n'
    '        }\n'
    '\n'
    '        function Clock() {\n'
    '            var nowTime = new Date();\n'
    '            var Hour_24 = nowTime.getHours();\n'
    '            var Hour_12 = Hour_24 % 12;\n'
    '            var Min  = set2fig( nowTime.getMinutes() );\n'
    '            // var Sec  = set2fig( nowTime.getSeconds() );\n'
    '            var clock = Hour_12 + ":" + Min;\n'
    '            document.getElementById("Clock").innerHTML = clock;\n'
    '        }\n'
    '\n'
    '        function Ampm() {\n'
    '            var nowTime = new Date();\n'
    '            var hour = nowTime.getHours();\n'
    '            var hourStr = hour < 12 ? "AM" : "PM";\n'
    '            document.getElementById("Ampm").innerHTML = hourStr;\n'
    '        }\n'
    '\n'
    '        function Calendar() {\n'
    '            // index の作成\n'
    '            var index_month = ["January", "February", "March", "April", "May", "Jun", "July", "Augast", "September", "October", "November", "December"];\n'
    '            var index_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];\n'
    '\n'
    '            var nowTime = new Date();\n'
    '            Month = index_month[nowTime.getMonth()];\n'
    '            var Day = nowTime.getDate();\n'
    '            Week = index_week[nowTime.getDay()];\n'
    '\n'
    '            var calendar = Week + ",\t" + Month +"\t"+ Day;\n'
    '            document.getElementById("Calendar").innerHTML = calendar;\n'
    '        }\n'
    '\n'
    '        setInterval("Clock()",1000);\n'
    '        setInterval("Calendar()",1000);\n'
    '        setInterval("Ampm()",1000);\n'
    '\n'
    '        </script>\n'
    '    </main>\n'
    '    <footer>\n'
    '        <p>\n'
    '            <small>\n'
    '                &copy; Mesurement System Laboratory, Kyoto Institute of Technology.\n'
    '            </small>\n'
    '        </p>\n'
    '    </footer>\n'
    '</body>\n'
    '\n'
    '</html>\n'
)
f.close()

# cssの生成
f = open('/var/www/html/style.css','w')
f.write(
    '.graph_co2 {\n'
	'background-image: radial-gradient(#f2f2f2 50%, transparent 31%), conic-gradient(#25A31D 0% ' + str(rate3) + '%, #BBBBBB ' + str(rate3) + '% 100%);\n'
    '\n'
    '}\n'
    '.graph_temp {\n'
	'background-image: radial-gradient(#f2f2f2 50%, transparent 31%), conic-gradient(#ff9933 0% ' + str(rate1) + '%, #BBBBBB ' + str(rate1) + '% 100%);\n'
    '}\n'
    '\n'
    '.graph_humidity {\n'
	'background-image: radial-gradient(#f2f2f2 50%, transparent 31%), conic-gradient(#457FD3 0% ' + str(rate2) + '%, #BBBBBB ' + str(rate2) + '% 100%);\n'
    '}\n'
)
f.close()