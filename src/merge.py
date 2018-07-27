import pickle

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

if __name__ == "__main__":
    with open("../data/bjpmres.pkl", "rb") as f:
        tmpres = pickle.load(f)
    with open("../data/bj_box.pkl", "rb") as f:
        box = pickle.load(f)
    
    res = ["test_id,PM2.5,PM10,O3\n"]
    for st in bjst:
        idx = bjst[st]
        for i in range(48):
            tmp = [tmpres[48 * idx + i][0], tmpres[48 * idx + i][1], 0]
            if (tmpres[48 * idx + i][0] < box[3 * idx][i % 24][0]):
                tmp[0] = box[3 * idx][i % 24][2]
            if (tmpres[48 * idx + i][0] > box[3 * idx][i % 24][1]):
                tmp[0] = box[3 * idx][i % 24][3]
            if (tmpres[48 * idx + i][1] < box[3 * idx + 1][i % 24][0]):
                tmp[1] = box[3 * idx + 1][i % 24][2]
            if (tmpres[48 * idx + i][1] > box[3 * idx + 1][i % 24][1]):
                tmp[1] = box[3 * idx + 1][i % 24][3]
            tmp[2] = box[3 * idx + 2][i % 24][2]
            res.append(",".join([st + "#" + str(i), str(tmp[0]), str(tmp[1]), str(tmp[2])]) + "\n")

    with open("../data/ldtmpres.pkl", "rb") as f:
        tmpres = pickle.load(f)
    with open("../data/ld_box.pkl", "rb") as f:
        box = pickle.load(f)
    for st in ldst:
        idx = ldst[st]
        for i in range(48):
            tmp = [tmpres[48 * idx + i][0], tmpres[48 * idx + i][1]]
            if (tmpres[48 * idx + i][0] < box[2 * idx][i % 24][0]):
                tmp[0] = box[2 * idx][i % 24][2]
            if (tmpres[48 * idx + i][0] > box[2 * idx][i % 24][1]):
                tmp[0] = box[2 * idx][i % 24][3]
            if (tmpres[48 * idx + i][1] < box[2 * idx + 1][i % 24][0]):
                tmp[1] = box[2 * idx + 1][i % 24][2]
            if (tmpres[48 * idx + i][1] > box[2 * idx + 1][i % 24][1]):
                tmp[1] = box[2 * idx + 1][i % 24][3]
            res.append(",".join([st + "#" + str(i), str(tmp[0]), str(tmp[1])]) + "\n")

    with open("../data/fixres.csv", "w") as f:
        f.writelines(res)
