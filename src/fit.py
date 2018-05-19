import pickle
import numpy
import time
import math
from sklearn.linear_model import LinearRegression

aqstations = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
            'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
            'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
            'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
            'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
            'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
            'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
            'dongsihuan_aq' : 34}

def getCoef(idx):
    tmpdata = numpy.zeros(l - 24)
    for i in range(24, l):
        tmpdata[i - 24] = dat[idx][i] - dat[idx][i - 24]
    for i in range(48, l):
        px[i - 48][0] = math.sin(i / 12 * math.pi)
        for j in range(1, 19):
            px[i - 48][j] = tmpdata[i - 42 + j]
    py = tmpdata[24:]
    linear = LinearRegression()
    linear.fit(px, py)
    res.append([linear.coef_, linear.intercept_])

if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        dat = pickle.load(f)
    l = len(dat[0])

    px = numpy.zeros((l - 48, 19), dtype = numpy.float32)

    res = []
    for st in aqstations:
        print(st)
        print("PM2.5")
        idx = aqstations[st] * 6 + 0
        getCoef(idx)

        print("PM10")
        idx = aqstations[st] * 6 + 1
        getCoef(idx)
        
        print("O3")
        idx = aqstations[st] * 6 + 4
        getCoef(idx)

    with open("../data/bjols_res.pkl", "wb") as f:
        pickle.dump(res, f)

aqstations = {'BL0':0, 'CD1':1, 'CD9':2, 'GN0':3, 'GN3':4, 'GR4':5, 'GR9':6, 'HV1':7, 'KF1':8, 'LW2':9,
                   'ST5':10, 'TH4':11, 'MY7':12}

if __name__ == "__main__":
    with open("../data/london_data.pkl", "rb") as f:
        dat = pickle.load(f)
    l = len(dat[0])

    px = numpy.zeros((l - 48, 19), dtype = numpy.float32)

    res = []
    for st in aqstations:
        print(st)
        print("PM2.5")
        idx = aqstations[st] * 3 + 0
        getCoef(idx)

        print("PM10")
        idx = aqstations[st] * 3 + 1
        getCoef(idx)

    with open("../data/ldols_res.pkl", "wb") as f:
        pickle.dump(res, f)
