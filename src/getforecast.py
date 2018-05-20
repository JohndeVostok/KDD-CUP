import pickle
import datetime
import numpy as np
from urllib import request
import math

SUFFIX = '/2k0d1d8'

n_meo = 5
n_grid = 651
london_n_grid = 861
meos = {'temperature' : 0, 'pressure' : 1, 'humidity' : 2, 'wind_direction' : 3, 'wind_speed' : 4}
endtimefp = open('../data/endtime')
raw_lines = endtimefp.readlines()
lines = [line.strip() for line in raw_lines]
bj_endtime = datetime.datetime.strptime(lines[0], '%Y-%m-%d %H:%M:%S')
ld_endtime = datetime.datetime.strptime(lines[1], '%Y-%m-%d %H:%M:%S')
endtimefp.close()

bj_length = n_grid * (n_meo - 1) + 18 + 1
ld_length = london_n_grid * (n_meo - 1) + 18 + 1

bj_width = 24 - (bj_endtime.hour + 1) + 24 + 24
ld_width = 24 - (ld_endtime.hour + 1) + 24 + 24

bj_data = np.zeros((bj_width, bj_length), dtype=np.float32)
ld_data = np.zeros((ld_width, ld_length), dtype=np.float32)

bj_startstr = str(bj_endtime.year) + '-' + str(bj_endtime.month) + '-' + str(bj_endtime.day - 1) + '-23'
ld_startstr = str(ld_endtime.year) + '-' + str(ld_endtime.month) + '-' + str(ld_endtime.day - 1) + '-23'

bj_forecast_url = 'http://kdd.caiyunapp.com/competition/forecast/bj/' + bj_startstr + SUFFIX
ld_forecast_url = 'http://kdd.caiyunapp.com/competition/forecast/ld/' + ld_startstr + SUFFIX

bj_forecast_res = request.urlopen(bj_forecast_url)
bj_forecast_content = bj_forecast_res.read()
bj_forecast_content = bj_forecast_content.decode(encoding='utf-8')
bj_forecast_lines = bj_forecast_content.split('\r\n')
bj_forecast_lines = bj_forecast_lines[1:-1]

for line in bj_forecast_lines:
    line_splited = line.split(',')
    stationid = line_splited[1]
    id_splited = stationid.split('_')
    urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
    temptime = datetime.datetime.strptime(str(bj_endtime.year) + '-' + str(bj_endtime.month) + '-' + str(bj_endtime.day),
                                          '%Y-%m-%d')
    urldelta = int((urltime - temptime).total_seconds() / 3600) + 24 - (bj_endtime.hour + 1)
    colume = (n_meo - 1) * int(id_splited[-1])
    bj_data[urldelta][colume] = float(line_splited[4])
    bj_data[urldelta][colume + 1] = float(line_splited[5])
    bj_data[urldelta][colume + 2] = float(line_splited[6])
    bj_data[urldelta][colume + 3] = float(line_splited[7])


ld_forecast_res = request.urlopen(ld_forecast_url)
ld_forecast_content = ld_forecast_res.read()
ld_forecast_content = ld_forecast_content.decode(encoding='utf-8')
ld_forecast_lines = ld_forecast_content.split('\r\n')
ld_forecast_lines = ld_forecast_lines[1:-1]

for line in ld_forecast_lines:
    line_splited = line.split(',')
    stationid = line_splited[1]
    id_splited = stationid.split('_')
    urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
    temptime = datetime.datetime.strptime(str(ld_endtime.year) + '-' + str(ld_endtime.month) + '-' + str(ld_endtime.day),
                                          '%Y-%m-%d')
    urldelta = int((urltime - temptime).total_seconds() / 3600) + 24 - (ld_endtime.hour + 1)
    colume = (n_meo - 1) * int(id_splited[-1])
    ld_data[urldelta][colume] = float(line_splited[4])
    ld_data[urldelta][colume + 1] = float(line_splited[5])
    ld_data[urldelta][colume + 2] = float(line_splited[6])
    ld_data[urldelta][colume + 3] = float(line_splited[7])


## 开始填真实数据
bj_history_startdate = bj_endtime - datetime.timedelta(days=1) + datetime.timedelta(hours=1)
ld_history_startdate = ld_endtime - datetime.timedelta(days=1) + datetime.timedelta(hours=1)

current_date = datetime.datetime.now()
current_str = str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day) +'-' \
                 + str(current_date.hour)

bj_grid_url = 'https://biendata.com/competition/meteorology/bj_grid/' + \
              bj_history_startdate.strftime('%Y-%m-%d-%H') + '/' + current_str + SUFFIX
ld_grid_url = 'https://biendata.com/competition/meteorology/ld_grid/' + \
              ld_history_startdate.strftime('%Y-%m-%d-%H') + '/' + current_str + SUFFIX

bj_grid_res = request.urlopen(bj_grid_url)
bj_grid_content = bj_grid_res.read()
bj_grid_content = bj_grid_content.decode(encoding='utf-8')
bj_grid_lines = bj_grid_content.split('\r\n')
bj_grid_lines = bj_grid_lines[1:-1]

for line in bj_grid_lines:
    line_splited = line.split(',')
    urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
    urldelta = int((urltime - bj_history_startdate).total_seconds() / 3600)
    stationid = line_splited[1]
    id_splited = stationid.split('_')
    colume = (n_meo - 1) * int(id_splited[-1])
    ld_data[urldelta][colume] = float(line_splited[4])
    ld_data[urldelta][colume + 1] = float(line_splited[5])
    ld_data[urldelta][colume + 2] = float(line_splited[6])
    ld_data[urldelta][colume + 3] = float(line_splited[8])

ld_grid_res = request.urlopen(ld_grid_url)
ld_grid_content = ld_grid_res.read()
ld_grid_content = ld_grid_content.decode(encoding='utf-8')
ld_grid_lines = ld_grid_content.split('\r\n')
ld_grid_lines = ld_grid_lines[1:-1]

for line in ld_grid_lines:
    line_splited = line.split(',')
    urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
    urldelta = int((urltime - ld_history_startdate).total_seconds() / 3600)
    stationid = line_splited[1]
    id_splited = stationid.split('_')
    colume = (n_meo - 1) * int(id_splited[-1])
    ld_data[urldelta][colume] = float(line_splited[4])
    ld_data[urldelta][colume + 1] = float(line_splited[5])
    ld_data[urldelta][colume + 2] = float(line_splited[6])
    ld_data[urldelta][colume + 3] = float(line_splited[8])

##处理sin

for i in range(24 - (bj_endtime.hour + 1)):
    bj_data[i][n_grid * (n_meo - 1)] = math.sin((i + bj_endtime.hour + 1) / 12 * math.pi)
for i in range(48):
    bj_data[24 - (bj_endtime.hour + 1) + i][n_grid * (n_meo - 1)] = math.sin((i % 24) / 12 * math.pi)

for i in range(24 - (ld_endtime.hour + 1)):
    ld_data[i][london_n_grid * (n_meo - 1)] = math.sin((i + ld_endtime.hour + 1) / 12 * math.pi)
for i in range(48):
    ld_data[24 - (ld_endtime.hour + 1) + i][london_n_grid * (n_meo - 1)] = math.sin((i % 24) / 12 * math.pi)

bjfp = open('../data/bj_forecast.pkl', 'wb')
pickle.dump(bj_data, bjfp)
bjfp.close()

ldfp = open('../data/ld_forecast.pkl', 'wb')
pickle.dump(ld_data, ldfp)
ldfp.close()