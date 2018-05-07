import pickle
import numpy
import time
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
    py = dat[idx]
    linear = LinearRegression()
    linear.fit(px, py)
    res.append(linear.coef_)
    res.append(linear.intercept_)

if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        dat = pickle.load(f)
    l = len(dat[0])
    tpx = [];
    for i in range(l):
        tpx.append([])
        for j in range(651):
            tpx[i].append(dat[300 + j * 5][i])
            tpx[i].append(dat[300 + j * 5 + 1][i])
            tpx[i].append(dat[300 + j * 5 + 2][i])
            tpx[i].append(dat[300 + j * 5 + 4][i])
    px = numpy.array(tpx).reshape(-1, 651 * 4)

    print("grid data initialized.")    

    res = []

    for st in aqstations:
        getCoef(aqstations[st] * 6)
        getCoef(aqstations[st] * 6 + 1)
        getCoef(aqstations[st] * 6 + 4)

    with open("../data/bjols_res.pkl", "wb") as f:
        pickle.dump(res, f)
