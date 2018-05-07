import numpy as np
import pickle
import requests

day = 7

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

def getans(idx, t, time):
	ans = data[(idx * 3 + t) * 2 + 1]
	for i in range(2064):
		ans += tmp[time][i] * data[(idx * 3 + t) * 2][i]
	return ans

if __name__ == "__main__":
	with open("../data/bjols_res.pkl", "rb") as f:
		data = pickle.load(f)
	url = "http://kdd.caiyunapp.com/competition/forecast/bj/2018-05-" + str(day) + "-11/2k0d1d8"
	resp = requests.get(url)
	tmplist = resp.text.split("\r\n")
	print(url)
	print(len(tmplist))

	tmp = np.array([entry.split(",")[4:8] for entry in tmplist[1:-1]]).reshape((651, 48, 4)).swapaxes(0, 1).reshape(48, -1)

	for st in bjst:
		for i in range(48):
			tmppm25 = getans(bjst[st], 0, i)
			tmppm10 = getans(bjst[st], 1, i)
			tmpo3 = getans(bjst[st], 2, i)
			res.append(','.join([st + "#" + str(i), tmppm25, tmppm10, tmpo3]) + "\n")
	with open("tmpres.csv", "w") as f:
		f.writelines(res)
