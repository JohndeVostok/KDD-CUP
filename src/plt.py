from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle
import numpy

bjst = {'dongsi_aq' : 0}

'''
bjst = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
            'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
            'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
            'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
            'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
            'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
            'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
            'dongsihuan_aq' : 34}
'''

if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        ori = pickle.load(f)

    res = []
    for st in bjst:
        data = [[] for i in range(24)]
        for idx, i in enumerate(ori[bjst[st] * 6 + 4]):
            if (i != 0):
                data[idx % 24].append(i)
        for entry in data:
            entry.sort()

        tmp = []
        for idx in range(24):
            l = len(data[idx])
            lq1 = int(l / 4)
            lq2 = int(l / 2)
            lq3 = int(l * 3 / 4)
            q1 = data[idx][lq1]
            q2 = data[idx][lq2]
            q3 = data[idx][lq3]
            iqr = q3 - q1
            mn = max([min(data[idx]), q1 - 1.5 * iqr])
            mx = min([max(data[idx]), q3 + 1.5 * iqr])
            tt = 0
            for i in data[idx]:
                if i > mx:
                    tt += 1
            tmp.append([mn, mx, q1, q3])
        res.append(tmp)
        
