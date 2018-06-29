import pickle
import numpy

from sklearn.preprocessing import MinMaxScaler

if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        data = pickle.load(f)
    with open("../data/meoaverage.pkl", "rb") as f:
        meo = pickle.load(f)
    n = data.shape[0]
    l = data.shape[1]

    bjst = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
            'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
            'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
            'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
            'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
            'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
            'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
            'dongsihuan_aq' : 34}

    tmp = data[0]
    s = 0
    t = 0
    mx = 0
    mn = 1000
    for i in range(l):
        if tmp[i] != 0:
            s += tmp[i]
            t += 1
            mx = max([mx, tmp[i]])
            mn = min([mn, tmp[i]])
    for i in range(len(tmp)):
        if tmp[i] == 0:
            tmp[i] = (s / t - mn) / (mx - mn)
        else:
            tmp[i] = (tmp[i] - mn) / (mx - mn)

    for i in range(4):
        s = 0
        t = 0
        mx = -10000
        mn = 10000
        for j in range(l):
            if meo[j][i] != 0:
                s += meo[j][i]
                t += 1
                mx = max([mx, meo[j][i]])
                mn = min([mn, meo[j][i]])
        for j in range(l):
            if meo[j][i] == 0:
                meo[j][i] = (s / t - mn) / (mx - mn)
            else:
                meo[j][i] = (meo[j][i] - mn) / (mx - mn)
#    scaler = MinMaxScaler(feature_range = (0, 1))
#    scaled = scaler.fit_transform(tmp.reshape(1, -1))
    scaled = tmp.reshape(1, -1)

    ltrain = 11618
    ntrain = int(ltrain / 24) - 4
    ltest = l - ltrain
    ntest = 31

    tmpx = numpy.zeros((ntrain, 48, 5))
    tmpy = numpy.zeros((ntrain, 48, 1))
    resx = numpy.zeros((ntest, 48, 5))
    resy = numpy.zeros((ntest, 48, 1))
    for i in range(ntrain):
        for j in range(48):
            tmpx[i][j][0] = scaled[0][i * 24 + j]
            tmpx[i][j][1] = meo[i * 24 + j + 48][0]
            tmpx[i][j][2] = meo[i * 24 + j + 48][1]
            tmpx[i][j][3] = meo[i * 24 + j + 48][2]
            tmpx[i][j][4] = meo[i * 24 + j + 48][3]
            tmpy[i][j] = scaled[0][i * 24 + j + 48]
    for i in range(ntest):
        for j in range(48):
            resx[i][j] = scaled[0][ltrain + i * 24 + j - 48]
            tmpx[i][j][1] = meo[ltrain + i * 24 + j][0]
            tmpx[i][j][2] = meo[ltrain + i * 24 + j][1]
            tmpx[i][j][3] = meo[ltrain + i * 24 + j][2]
            tmpx[i][j][4] = meo[ltrain + i * 24 + j][3]
            resy[i][j] = scaled[0][ltrain + i * 24 + j]
    with open("../data/netdata.pkl", "wb") as f:
        pickle.dump([tmpx, tmpy, resx, resy], f)
