import pickle
import math

dt = 48

bjst = {'dongsi_aq' : 0}
ldst = {}

'''
bjst = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
            'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
            'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
            'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
            'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
            'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
            'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
            'dongsihuan_aq' : 34}

ldst = {'BL0':0, 'CD1':1, 'CD9':2, 'GN0':3, 'GN3':4, 'GR4':5, 'GR9':6, 'HV1':7, 'KF1':8, 'LW2':9,
                   'ST5':10, 'TH4':11, 'MY7':12}
'''

def getans(idx, idy):
    ans = []
    l = len(data[idx])
    tmp = [0]
    ori = []
    for i in range(18):
        tmp.append(data[idx][l - 18 + i] - data[idx][l - 42 + i])
    for i in range(24):
        ori.append(data[idx][l - 24 + i])
    for i in range(dt):
        tmp[0] = math.sin(l / 12 * math.pi)
        t = ols[idy][1]
        for j in range(19):
            t += tmp[j] * ols[idy][0][j]
        ans.append(t)
        for j in range(1, 18):
            tmp[j] = tmp[j + 1]
            tmp[18] = t
    print(ans[0], ori[0])
    for i in range(24):
        ans[i] += ori[i]
    for i in range(24, dt):
        ans[i] += ans[i - 24]
    return ans

if __name__ == "__main__":
    res = []
    with open("../data/beijing_data.pkl", "rb") as f:
        data = pickle.load(f)
    with open("../data/bjols_res.pkl", "rb") as f:
        ols = pickle.load(f)
    for st in bjst:
        #PM2.5
        idx = 6 * bjst[st] + 0
        idy = 3 * bjst[st] + 0
        tmp0 = getans(idx, idy);
        #PM10
        idx = 6 * bjst[st] + 1
        idy = 3 * bjst[st] + 1
        tmp1 = getans(idx, idy);
        #O3
        idx = 6 * bjst[st] + 4
        idy = 3 * bjst[st] + 2
        tmp2 = getans(idx, idy);
        for i in range(48):
            res.append(','.join([st + "#" + str(i), str(tmp0[dt - 48 + i]), str(tmp1[dt - 48 + i]), str(tmp2[dt - 48 + i])]) + "\n")

    with open("../data/london_data.pkl", "rb") as f:
        data = pickle.load(f)
    with open("../data/ldols_res.pkl", "rb") as f:
        ols = pickle.load(f)
    for st in ldst:
        #PM2.5
        idx = 3 * ldst[st] + 0
        idy = 2 * ldst[st] + 0
        tmp0 = getans(idx, idy);
        #PM10
        idx = 3 * ldst[st] + 1
        idy = 2 * ldst[st] + 1
        tmp0 = getans(idx, idy);
        for i in range(48):
            res.append(','.join([st + "#" + str(i), str(tmp0[dt - 48 + i]), str(tmp1[dt - 48 + i]), str(tmp2[dt - 48 + i])]) + "\n")

    with open("../data/tmpres.csv", "w") as f:
        f.writelines(res)
