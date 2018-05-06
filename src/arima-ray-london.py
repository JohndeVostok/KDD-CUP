import ray
import csv
import numpy
import pickle
import statsmodels.api as sm

bjsts = {'dongsi_aq' : 0, 'tiantan_aq' : 1, 'guanyuan_aq' : 2, 'wanshouxigong_aq' : 3, 'aotizhongxin_aq' : 4,
            'nongzhanguan_aq' : 5, 'wanliu_aq' : 6, 'beibuxinqu_aq' : 7, 'zhiwuyuan_aq' : 8, 'fengtaihuayuan_aq' : 9,
            'yungang_aq' : 10, 'gucheng_aq' : 11, 'fangshan_aq' : 12, 'daxing_aq' : 13, 'yizhuang_aq' : 14,
            'tongzhou_aq' : 15, 'shunyi_aq' : 16, 'pingchang_aq' : 17, 'mentougou_aq' : 18, 'pinggu_aq' : 19,
            'huairou_aq' : 20, 'miyun_aq' : 21, 'yanqin_aq' : 22, 'dingling_aq' : 23, 'badaling_aq' : 24,
            'miyunshuiku_aq' : 25, 'donggaocun_aq' : 26, 'yongledian_aq' : 27, 'yufa_aq' : 28, 'liulihe_aq' : 29,
            'qianmen_aq' : 30, 'yongdingmennei_aq' : 31, 'xizhimenbei_aq' : 32, 'nansanhuan_aq' : 33,
            'dongsihuan_aq' : 34}

bjaqs = {'PM2.5' : 0, 'PM10' : 1, 'NO2' : 2, 'CO' : 3, 'O3' : 4, 'SO2' : 5}

ldsts = {'BL0':0, 'CD1':1, 'CD9':2, 'GN0':3, 'GN3':4, 'GR4':5, 'GR9':6, 'HV1':7, 'KF1':8, 'LW2':9,
                   'ST5':10, 'TH4':11, 'MY7':12, 'BX1':13, 'BX9':14, 'CT2':15, 'CT3':16, 'CR8':17, 'GB0':18,
                   'HR1':19, 'LH0':20, 'KC1':21, 'RB7':22, 'TD5':23}

ldaqs = {'PM2.5' : 0, 'PM10' : 1, 'NO2' : 2}

@ray.remote
def getPre(idx, name):
	tmpdata = data[idx].copy()
	l = len(tmpdata)
	dd = 24
	td = []
	for i in range(dd, l):
		td.append(tmpdata[i] - tmpdata[i - dd])
	tmpdata = numpy.array(td)
	
	ml = sm.tsa.ARMA(tmpdata, (18, 3)).fit()

	with open(name + ".pkl", "wb") as f:
		pickle.dump(ml, f)
	
	pre = ml.predict(len(tmpdata), len(tmpdata) + 96, dynamic = True)
	tmpd = list(tmpdata)
	for i in pre:
		tmpd.append(tmpd[-48] + i)
		if tmpd[-1] < 0:
			tmpd[-1] = 0
	res.append([name, tmpd[-96:]])
	return 1

with open("../data/london_data.pkl", "rb") as f:
	data = pickle.load(f)

res = []
waitList = []

ray.init()

for st in ldsts:
	n0 = bjsts[st] * 3;
	waitList.append(getPre.remote(n0, st+"PM25"))
	n1 = n0 + 1
	waitList.append(getPre.remote(n1, st+"PM10"))

for i in waitList:
	suc = ray.get(i)

with open("ldres.pkl", "wb") as f:
	pickle.dump(res, f)
