import pickle
import numpy
import time
#from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

aqstations = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
			'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
			'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
			'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
			'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
			'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
			'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
			'dongsihuan_aq' : 34}

if __name__ == "__main__":
	with open("../data/beijing_data.pkl", "rb") as f:
		dat = pickle.load(f)

	l = len(dat[4])
	tmpdata = numpy.zeros(l - 24)

	for i in range(l - 24):
		if dat[4][i + 24] == 0:
			tmpdata[i] = 0
		elif dat[4][i] == 0:
			tmpdata[i] = 0
		else:
			tmpdata[i] = dat[4][i + 24] - dat[4][i]
	
	tmpnum = numpy.zeros(24)
	tmpsum = numpy.zeros(24)

	for i in range(l - 24):
		if (tmpdata[i] != 0):
			tmpnum[i % 24] += 1
			tmpsum[i % 24] += tmpdata[i]

	lp = 0
	res = []
	for i in dat[4]:
		if (i == 0):
			lp += 1
		else:
			if (lp != 0):
				res.append(lp)
			lp = 0
	print(res)
	s = sum([tmpsum[i] / tmpnum[i] for i in range(24)])
	print(s)
	plt.plot(range(24), [tmpsum[i] / tmpnum[i] for i in range(24)])
	plt.show()
