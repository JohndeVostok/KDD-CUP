import datetime
import pickle
import numpy as np
from urllib import request

SUFFIX = '/2k0d1d8'

n_types = 6
n_meo = 5
n_grid = 651
n_aqstation = 35
n_weatherstation = 18

aqs = {'PM2.5' : 0, 'PM10' : 1, 'NO2' : 2, 'CO' : 3, 'O3' : 4, 'SO2' : 5}
meos = {'temperature' : 0, 'pressure' : 1, 'humidity' : 2, 'wind_direction' : 3, 'wind_speed' : 4}

aqstations = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
            'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
            'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
            'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
            'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
            'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
            'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
            'dongsihuan_aq' : 34}

weatherstations = {'beijing_meo' : 0, 'chaoyang_meo' : 1, 'daxing_meo' : 2, 'fangshan_meo' : 3, 'fengtai_meo' : 4,
                   'hadian_meo' : 5, 'huairou_meo' : 6, 'mentougou_meo' : 7, 'miyun_meo' : 8, 'pingchang_meo' : 9,
                   'pinggu_meo' : 10, 'shangdianzi_meo' : 11, 'shijingshan_meo' : 12, 'shunyi_meo' : 13,
                   'tongzhou_meo' : 14, 'xiayunling_meo' : 15, 'yanqing_meo' : 16, 'zhaitang_meo' : 17}

Length = n_aqstation * n_types + n_weatherstation * n_meo + n_grid * n_meo

london_n_types = 3
london_n_grid = 861
n_forecast_station = 13
n_other_station = 11

london_stations = {'BL0':0, 'CD1':1, 'CD9':2, 'GN0':3, 'GN3':4, 'GR4':5, 'GR9':6, 'HV1':7, 'KF1':8, 'LW2':9,
                   'ST5':10, 'TH4':11, 'MY7':12, 'BX1':13, 'BX9':14, 'CT2':15, 'CT3':16, 'CR8':17, 'GB0':18,
                   'HR1':19, 'LH0':20, 'KC1':21, 'RB7':22, 'TD5':23}

london_Length = (n_forecast_station + n_other_station) * 3 + london_n_grid * n_meo

if __name__ == "__main__":

    endtimefp = open('../data/newendtime')
    beijing_str = endtimefp.readline()
    beijing_str = beijing_str[:-1]
    london_str = endtimefp.readline()
    london_str = london_str[:-1]
    endtimefp.close()

    beijing_endtime = datetime.datetime.strptime(beijing_str, '%Y-%m-%d %H:%M:%S')
    beijing_starttime = beijing_endtime + datetime.timedelta(hours=1)
    london_endtime = datetime.datetime.strptime(london_str, '%Y-%m-%d %H:%M:%S')
    london_starttime = london_endtime + datetime.timedelta(hours=1)

    beijingfp = open('../data/beijing_data.pkl', 'rb')
    beijing_data = pickle.load(beijingfp)
    beijingfp.close()

    londonfp = open('../data/london_data.pkl', 'rb')
    london_data = pickle.load(londonfp)
    londonfp.close()

    current_date = datetime.datetime.now()
    current_str = str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day) +'-' \
                    + str(current_date.hour)

    ### For Beijing ###
    bj_start_str = str(beijing_starttime.year) + '-' + str(beijing_starttime.month) + '-' + str(beijing_starttime.day) \
                    + '-' + str(beijing_starttime.hour)
    bj_aq_url = 'https://biendata.com/competition/airquality/bj/' + bj_start_str + '/' + current_str + SUFFIX
    bj_meo_url = 'https://biendata.com/competition/meteorology/bj/' + bj_start_str + '/' + current_str + SUFFIX
    bj_grid_url = 'https://biendata.com/competition/meteorology/bj_grid/' + bj_start_str + '/' + current_str + SUFFIX

    bj_end_dates = []

    bj_aq_res = request.urlopen(bj_aq_url)
    bj_aq_content = bj_aq_res.read()
    bj_aq_content = bj_aq_content.decode(encoding='utf-8')
    bj_aq_lines = bj_aq_content.split('\r\n')
    bj_aq_lines = bj_aq_lines[1:-1]
    if bj_aq_lines:
        templine = bj_aq_lines[-1]
        tempsplited = templine.split(',')
        temptime = datetime.datetime.strptime(tempsplited[2], '%Y-%m-%d %H:%M:%S')
        bj_end_dates.append(temptime)

    bj_meo_res = request.urlopen(bj_meo_url)
    bj_meo_content = bj_meo_res.read()
    bj_meo_content = bj_meo_content.decode(encoding='utf-8')
    bj_meo_lines = bj_meo_content.split('\r\n')
    bj_meo_lines = bj_meo_lines[1:-1]
    if bj_meo_lines:
        templine = bj_meo_lines[-1]
        tempsplited = templine.split(',')
        temptime = datetime.datetime.strptime(tempsplited[2], '%Y-%m-%d %H:%M:%S')
        bj_end_dates.append(temptime)

    bj_grid_res = request.urlopen(bj_grid_url)
    bj_grid_content = bj_grid_res.read()
    bj_grid_content = bj_grid_content.decode(encoding='utf-8')
    bj_grid_lines = bj_grid_content.split('\r\n')
    bj_grid_lines = bj_grid_lines[1:-1]
    if bj_grid_lines:
        templine = bj_grid_lines[-1]
        tempsplited = templine.split(',')
        temptime = datetime.datetime.strptime(tempsplited[2], '%Y-%m-%d %H:%M:%S')
        bj_end_dates.append(temptime)

    bj_end_date = max(bj_end_dates)

    bj_update_hours = 24 * (bj_end_date - beijing_starttime).days + 1 + bj_end_date.hour + 24 - beijing_starttime.hour
    bj_update_data  = np.zeros((Length, bj_update_hours), dtype=np.float32)

    for line in bj_aq_lines:
        line_splited = line.split(',')
        urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
        urldelta = (urltime - beijing_starttime).days * 24 + urltime.hour - beijing_starttime.hour
        row = aqstations[line_splited[1]] * n_types
        for i in range(6):
            if line_splited[3 + i]:
                bj_update_data[row + i][urldelta] = float(line_splited[3 + i])

    print('Update Beijing Air Quality')

    for line in bj_meo_lines:
        line_splited = line.split(',')
        urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
        urldelta = (urltime - beijing_starttime).days * 24 + urltime.hour - beijing_starttime.hour
        row = weatherstations[line_splited[1]] * n_meo
        for i in range(3):
            if line_splited[4 + i]:
                bj_update_data[row + i][urldelta] = float(line_splited[4 + i])
            if line_splited[7]:
                bj_update_data[row + 4][urldelta] = float(line_splited[7])
            if line_splited[8]:
                bj_update_data[row + 3][urldelta] = float(line_splited[8])

    print('Update Beijing Meo')

    for line in bj_grid_lines:
        line_splited = line.split(',')
        urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
        urldelta = (urltime - beijing_starttime).days * 24 + urltime.hour - beijing_starttime.hour
        stationid = line_splited[1]
        id_splited = stationid.split('_')
        row = n_aqstation * n_types + n_weatherstation * n_meo + int(id_splited[-1]) * n_meo
        for i in range(5):
            if line_splited[4 + i]:
                bj_update_data[row + i][urldelta] = float(line_splited[4 + i])

    print('Update Beijing Grid')


    ### For London ###

    ld_start_str = str(london_starttime.year) + '-' + str(london_starttime.month) + '-' + str(london_starttime.day) \
                   + '-' + str(london_starttime.hour)
    ld_aq_url = 'https://biendata.com/competition/airquality/ld/' + ld_start_str + '/' + current_str + SUFFIX
    ld_grid_url = 'https://biendata.com/competition/meteorology/ld_grid/' + ld_start_str + '/' + current_str + SUFFIX

    ld_end_dates = []

    ld_aq_res = request.urlopen(ld_aq_url)
    ld_aq_content = ld_aq_res.read()
    ld_aq_content = ld_aq_content.decode(encoding='utf-8')
    ld_aq_lines = ld_aq_content.split('\r\n')
    ld_aq_lines = ld_aq_lines[1:-1]
    if ld_aq_lines:
        templine = ld_aq_lines[-1]
        tempsplited = templine.split(',')
        temptime = datetime.datetime.strptime(tempsplited[2], '%Y-%m-%d %H:%M:%S')
        ld_end_dates.append(temptime)

    ld_grid_res = request.urlopen(ld_grid_url)
    ld_grid_content = ld_grid_res.read()
    ld_grid_content = ld_grid_content.decode(encoding='utf-8')
    ld_grid_lines = ld_grid_content.split('\r\n')
    ld_grid_lines = ld_grid_lines[1:-1]
    if ld_grid_lines:
        templine = ld_grid_lines[-1]
        tempsplited = templine.split(',')
        temptime = datetime.datetime.strptime(tempsplited[2], '%Y-%m-%d %H:%M:%S')
        ld_end_dates.append(temptime)

    ld_end_date = max(ld_end_dates)

    ld_update_hours = 24 * (ld_end_date - london_starttime).days + 1 + ld_end_date.hour + 24 - london_starttime.hour
    ld_update_data = np.zeros((london_Length, ld_update_hours), dtype=np.float32)

    for line in ld_aq_lines:
        line_splited = line.split(',')
        urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
        urldelta = (urltime - london_starttime).days * 24 + urltime.hour - london_starttime.hour
        row = london_stations[line_splited[1]] * london_n_types
        for i in range(3):
            if line_splited[3 + i]:
                ld_update_data[row + i][urldelta] = float(line_splited[3 + i])

    print('Update London Air Quality')

    for line in ld_grid_lines:
        line_splited = line.split(',')
        urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
        urldelta = (urltime - london_starttime).days * 24 + urltime.hour - london_starttime.hour
        stationid = line_splited[1]
        id_splited = stationid.split('_')
        row = london_n_types * (n_forecast_station + n_other_station) + int(id_splited[-1]) * n_meo
        for i in range(5):
            if line_splited[4 + i]:
                ld_update_data[row + i][urldelta] = float(line_splited[4 + i])

    print('Update London Grid')

    endtimefp = open('../data/newendtime', 'w')
    endtimefp.write(bj_end_date.strftime('%Y-%m-%d %H:%M:%S'))
    endtimefp.write('\n')
    endtimefp.write(ld_end_date.strftime('%Y-%m-%d %H:%M:%S'))
    endtimefp.write('\n')
    endtimefp.close()

    beijingfp = open('../data/new_beijing_data.pkl', 'wb')
    beijing_data = pickle.dump(np.concatenate((beijing_data, bj_update_data), axis=1), beijingfp)
    beijingfp.close()

    londonfp = open('../data/new_london_data.pkl', 'wb')
    london_data = pickle.dump(np.concatenate((london_data, ld_update_data), axis=1), londonfp)
    londonfp.close()

    print(bj_end_date)
    print(ld_end_date)



