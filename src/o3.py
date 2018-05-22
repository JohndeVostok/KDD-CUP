from sklearn.linear_model import LinearRegression
import pickle
import numpy
import math

bjst = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
            'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
            'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
            'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
            'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
            'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
            'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
            'dongsihuan_aq' : 34}

if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        ori = pickle.load(f)

    l = ori.shape[1]
    z = numpy.zeros(l)
    tmp = numpy.zeros((l, 651 * 4 + 1))
    for i in range(l):
        for j in range(651):
            tmp[i][j * 4] = ori[300 + j * 5][i]
            tmp[i][j * 4 + 1] = ori[300 + j * 5 + 1][i]
            tmp[i][j * 4 + 2] = ori[300 + j * 5 + 2][i]
            tmp[i][j * 4 + 3] = ori[300 + j * 5 + 4][i]
            if (tmp[i][j * 4] == 0):
                z[i] = 1
                break
            if (tmp[i][j * 4 + 1] == 0):
                z[i] = 1
                break
            if (tmp[i][j * 4 + 2] == 0):
                z[i] = 1
                break
            if (tmp[i][j * 4 + 3] == 0):
                z[i] = 1
                break
        tmp[i][651 * 4] = math.cos(i / 12 * math.pi)
    res = []
    for st in bjst:
        print(st)
        idx = bjst[st] * 6 + 4
        px = []
        py = []
        for i in range(l):
            if (z[i] == 0 and ori[idx][i] != 0):
                px.append(tmp[i])
                py.append(ori[idx][i])
        linear = LinearRegression()
        linear.fit(px, py)
        res.append([linear.coef_, linear.intercept_])

    with open("../data/o3res.pkl", "wb") as f:
        pickle.dump(res, f)
