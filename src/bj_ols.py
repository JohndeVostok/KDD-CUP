import pickle
import numpy
import time
import math
from sklearn.linear_model import LinearRegression

#aqstations = {'dongsi_aq' : 0}

aqstations = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
			'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
			'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
			'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
			'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
			'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
			'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
			'dongsihuan_aq' : 34}

def getCoef(idx):
	py = tmpdata[24:]
	linear = LinearRegression()
	linear.fit(px, py)
	res.append([linear.coef_, linear.intercept_])

if __name__ == "__main__":
	with open("../data/beijing_data.pkl", "rb") as f:
		dat = pickle.load(f)
	l = len(dat[0])

	px = numpy.zeros(((l - 48), (651 * 4 + 19)), dtype = numpy.float32)
	for i in range(48, l):
		for j in range(651):
			px[i - 48][j * 4] = dat[300 + j * 5][i - 24]
			px[i - 48][j * 4 + 1] = dat[300 + j * 5 + 1][i - 24]
			px[i - 48][j * 4 + 2] = dat[300 + j * 5 + 2][i - 24]
			px[i - 48][j * 4 + 3] = dat[300 + j * 5 + 4][i - 24]


	for st in aqstations:
		idx = aqstations[st]
		tmpdata = numpy.zeros(l - 24)
		for i in range(24, l):
			tmpdata[i - 24] = dat[idx][i] - dat[idx][i - 24]

		for i in range(48, l):
			px[i - 48][651 * 4] = math.sin(i / 12 * math.pi)
			for j in range(1, 19):
				px[i - 48][651 * 4 + j] = tmpdata[i - 24 - j]

		res = []
		print(st + "initialized.")
		print("PM2.5")
		getCoef(aqstations[st] * 6 + 0)
		print("PM10")
		getCoef(aqstations[st] * 6 + 1)
		print("O3")
		getCoef(aqstations[st] * 6 + 4)
		print(st + "finished.")

	with open("../data/bjols_res.pkl", "wb") as f:
		pickle.dump(res, f)
