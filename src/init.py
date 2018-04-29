import csv
import numpy as np
import datetime
import pickle
from urllib import request

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
starttime = datetime.datetime.strptime('2017-01-01 0:00:00', '%Y-%m-%d %H:%M:%S')
endtime = datetime.datetime.strptime('2018-04-01 0:00:00', '%Y-%m-%d %H:%M:%S')
Hours = 24 * (endtime - starttime).days + 1 + endtime.hour
data = np.zeros((Length, Hours), np.float32)


with open('../data/beijing_17_18_aq.csv') as aqfile_1718:
    with open('../data/beijing_17_18_meo.csv') as meofile_1718:
        with open('../data/beijing_201802_201803_aq.csv') as aqfile_0203:
            with open('../data/beijing_201802_201803_me.csv') as meofile_0203:
                with open('../data/Beijing_historical_meo_grid.csv') as gridfile:
                    with open('../data/beijing_data.pkl', 'wb') as outputfile:

                        reader_aq_1718 = csv.DictReader(aqfile_1718)
                        for item in reader_aq_1718:
                            temptime = datetime.datetime.strptime(item['utc_time'], '%Y-%m-%d %H:%M:%S')
                            timedelta = (temptime - starttime).days * 24 + temptime.hour
                            baserow = aqstations[item['stationId']] * n_types
                            for each in aqs:
                                if item[each]:
                                    data[baserow + aqs[each]][timedelta] = float(item[each])
                        print('finish aq1718')

                        reader_aq_0203 = csv.DictReader(aqfile_0203)
                        for item in reader_aq_0203:
                            temptime = datetime.datetime.strptime(item['utc_time'], '%Y-%m-%d %H:%M:%S')
                            timedelta = (temptime - starttime).days * 24 + temptime.hour
                            baserow = aqstations[item['stationId']] * n_types
                            for each in aqs:
                                if item[each]:
                                    data[baserow + aqs[each]][timedelta] = float(item[each])
                        print('finish aq0203')

                        aqurl = 'http://biendata.com/competition/airquality/bj/2018-03-31-16/2018-04-01-0/2k0d1d8'
                        aqres = request.urlopen(aqurl)
                        aqcontent = aqres.read()
                        aqcontent = aqcontent.decode(encoding='utf-8')
                        aqlines = aqcontent.split('\r\n')
                        aqlines = aqlines[1:-1]
                        for line in aqlines:
                            line_splited = line.split(',')
                            urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
                            urldelta = (urltime - starttime).days * 24 + urltime.hour
                            row = aqstations[line_splited[1]] * n_types
                            for i in range(6):
                                if line_splited[3 + i]:
                                    data[row + i][urldelta] = float(line_splited[3 + i])


                        reader_meo_1718 = csv.DictReader(meofile_1718)
                        for item in reader_meo_1718:
                            temptime = datetime.datetime.strptime(item['utc_time'], '%Y-%m-%d %H:%M:%S')
                            timedelta = (temptime - starttime).days * 24 + temptime.hour
                            baserow = n_aqstation * n_types + weatherstations[item['station_id']] * n_meo
                            for each in meos:
                                if item[each]:
                                    data[baserow + meos[each]][timedelta] = float(item[each])
                        print('finish meo1718')

                        reader_meo_0203 = csv.DictReader(meofile_0203)
                        for item in reader_meo_0203:
                            temptime = datetime.datetime.strptime(item['utc_time'], '%Y-%m-%d %H:%M:%S')
                            timedelta = (temptime - starttime).days * 24 + temptime.hour
                            baserow = n_aqstation * n_types + weatherstations[item['station_id']] * n_meo
                            for each in meos:
                                if item[each]:
                                    data[baserow + meos[each]][timedelta] = float(item[each])
                        print('finish meo0203')

                        reader_grid = csv.DictReader(gridfile)
                        for item in reader_grid:
                            temptime = datetime.datetime.strptime(item['utc_time'], '%Y/%m/%d %H:%M')
                            timedelta = (temptime - starttime).days * 24 + temptime.hour
                            splited = item['stationName'].split('_')
                            temp = int(splited[-1])
                            baserow = n_aqstation * n_types + n_weatherstation * n_meo + temp * n_meo
                            for each in meos:
                                if item[each]:
                                    data[baserow + meos[each]][timedelta] = float(item[each])
                        print('finish grid')

                        meourl = 'http://biendata.com/competition/meteorology/bj_grid/2018-03-27-6/2018-04-01-0/2k0d1d8'
                        meores = request.urlopen(meourl)
                        meocontent = meores.read()
                        meocontent = meocontent.decode(encoding='utf-8')
                        meolines = meocontent.split('\r\n')
                        meolines = meolines[1:-1]
                        for line in meolines:
                            line_splited = line.split(',')
                            urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
                            urldelta = (urltime - starttime).days * 24 + urltime.hour
                            stationid = line_splited[1]
                            id_splited = stationid.split('_')
                            row = n_aqstation * n_types + n_weatherstation * n_meo + int(id_splited[-1]) * n_meo
                            for i in range(5):
                                if line_splited[4 + i]:
                                    data[row + i][urldelta] = float(line_splited[4 + i])

                        pickle.dump(data, outputfile)

                        aqfile_1718.close()
                        aqfile_0203.close()
                        meofile_1718.close()
                        meofile_0203.close()
                        gridfile.close()
                        outputfile.close()


london_n_types = 3
london_n_grid = 861
n_forecast_station = 13
n_other_station = 11

london_sttime = datetime.datetime.strptime('2017-01-01 0:00:00', '%Y-%m-%d %H:%M:%S')
london_endtime = datetime.datetime.strptime('2018-03-31 23:00:00', '%Y-%m-%d %H:%M:%S')
london_hours = 24 * (london_endtime - london_sttime).days + 1 + london_endtime.hour
london_Length = (n_forecast_station + n_other_station) * 3 + london_n_grid * n_meo
london_data = np.zeros((london_Length, london_hours), np.float32)

london_stations = {'BL0':0, 'CD1':1, 'CD9':2, 'GN0':3, 'GN3':4, 'GR4':5, 'GR9':6, 'HV1':7, 'KF1':8, 'LW2':9,
                   'ST5':10, 'TH4':11, 'MY7':12, 'BX1':13, 'BX9':14, 'CT2':15, 'CT3':16, 'CR8':17, 'GB0':18,
                   'HR1':19, 'LH0':20, 'KC1':21, 'RB7':22, 'TD5':23}


with open('../data/London_historical_aqi_forecast_stations_20180331.csv') as forecastfile:
    with open('../data/London_historical_aqi_other_stations_20180331.csv') as otherfile:
        with open('../data/London_historical_meo_grid.csv') as londongridfile:
            with open('../data/london_data.pkl', 'wb') as londonoutfile:

                forereader = csv.DictReader(forecastfile)
                for item in forereader:
                    temptime = datetime.datetime.strptime(item['MeasurementDateGMT'], '%Y/%m/%d %H:%M')
                    timedelta = (temptime - london_sttime).days * 24 + temptime.hour
                    baserow = london_stations[item['station_id']] * london_n_types
                    if item['PM2.5']:
                        london_data[baserow + aqs['PM2.5']][timedelta] = float(item['PM2.5'])
                    if item['PM10']:
                        london_data[baserow + aqs['PM10']][timedelta] = float(item['PM10'])
                    if item['NO2']:
                        london_data[baserow + aqs['NO2']][timedelta] = float(item['NO2'])
                print('finish london forecast')

                ldaqurl = 'http://biendata.com/competition/airquality/ld/2018-03-31-0/2018-03-31-23/2k0d1d8'
                ldaqres = request.urlopen(ldaqurl)
                ldaqcontent = ldaqres.read()
                ldaqcontent = ldaqcontent.decode(encoding='utf-8')
                ldaqlines = ldaqcontent.split('\r\n')
                ldaqlines = ldaqlines[1:-1]
                for line in ldaqlines:
                    line_splited = line.split(',')
                    urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
                    urldelta = (urltime - london_sttime).days * 24 + urltime.hour
                    row = london_stations[line_splited[1]] * london_n_types
                    for i in range(3):
                        if line_splited[3 + i]:
                            london_data[row + i][urldelta] = float(line_splited[3 + i])


                otherreader = csv.DictReader(otherfile)
                count = 0
                for item in otherreader:
                    count += 1
                    temptime = datetime.datetime.strptime(item['MeasurementDateGMT'], '%Y/%m/%d %H:%M')
                    timedelta = (temptime - london_sttime).days * 24 + temptime.hour
                    baserow = london_stations[item['Station_ID']] * london_n_types
                    if item['PM2.5']:
                        london_data[baserow + aqs['PM2.5']][timedelta] = float(item['PM2.5'])
                    if item['PM10']:
                        london_data[baserow + aqs['PM10']][timedelta] = float(item['PM10'])
                    if item['NO2']:
                        london_data[baserow + aqs['NO2']][timedelta] = float(item['NO2'])
                    if count == 118674:
                        break

                print('finish london other')

                londongridreader = csv.DictReader(londongridfile)
                for item in londongridreader:
                    temptime = datetime.datetime.strptime(item['utc_time'], '%Y-%m-%d %H:%M:%S')
                    timedelta = (temptime - london_sttime).days * 24 + temptime.hour
                    splited = item['stationName'].split('_')
                    temp = int(splited[-1])
                    baserow = 3 * (n_forecast_station + n_other_station) + temp * n_meo
                    for each in meos:
                        if item[each]:
                            london_data[baserow + meos[each]][timedelta] = float(item[each])
                print('finish london grid')

                ldmeourl = 'http://biendata.com/competition/meteorology/ld_grid/2018-03-27-6/2018-03-31-23/2k0d1d8'
                ldmeores = request.urlopen(ldmeourl)
                ldmeocontent = ldmeores.read()
                ldmeocontent = ldmeocontent.decode(encoding='utf-8')
                ldmeolines = ldmeocontent.split('\r\n')
                ldmeolines = ldmeolines[1:-1]
                for line in ldmeolines:
                    line_splited = line.split(',')
                    urltime = datetime.datetime.strptime(line_splited[2], '%Y-%m-%d %H:%M:%S')
                    urldelta = (urltime - london_sttime).days * 24 + urltime.hour
                    stationid = line_splited[1]
                    id_splited = stationid.split('_')
                    row = london_n_types * (n_forecast_station + n_other_station) + int(id_splited[-1]) * n_meo
                    for i in range(5):
                        if line_splited[4 + i]:
                            london_data[row + i][urldelta] = float(line_splited[4 + i])

                pickle.dump(london_data, londonoutfile)

                forecastfile.close()
                otherfile.close()
                londongridfile.close()
                londonoutfile.close()
