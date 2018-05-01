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

res = [["test_id", "PM2.5", "PM10", "O3"]]

with open("../pkl/beijing_data.pkl", "rb") as f:
    data = pickle.load(f)

for st in bjsts:
	n0 = bjsts[st] * 6;
	n1 = n0 + 1
	n2 = n0 + 4
	d0 = data[n0].copy();
	d1 = data[n1].copy();
	d2 = data[n2].copy();

	l = len(d0)
	dd = 24
	td0 = []
	td1 = []
	td2 = []
	l = len(dat)
	for i in range(dd, l):
		td0.append(d0[i] - d0[i - dd])
		td1.append(d1[i] - d1[i - dd])
		td2.append(d2[i] - d2[i - dd])
	d0 = numpy.array(td0)
	d1 = numpy.array(td1)
	d2 = numpy.array(td2)

	m0 = sm.tsa.ARMA(d0, (18, 3)).fit()
	m1 = sm.tsa.ARMA(d1, (18, 3)).fit()
	m2 = sm.tsa.ARMA(d2, (18, 3)).fit()

	p0 = m0.predict(len(d0), len(d0) + 48, dynamic = True)
	p1 = m1.predict(len(d1), len(d1) + 48, dynamic = True)
	p2 = m2.predict(len(d2), len(d2) + 48, dynamic = True)

	tr0 = []
	for i in range(24):
		tr0.append(p0[i] + data[n0][i - len(data[n0])])
	for i in range(24):
		tr0.append(p0[i + 24] + tr0[i])
	tr1 = []
	for i in range(24):
		tr1.append(p1[i] + data[n1][i - len(data[n1])])
	for i in range(24):
		tr1.append(p1[i + 24] + tr1[i])
	tr2 = []
	for i in range(24):
		tr2.append(p2[i] + data[n2][i - len(data[n2])])
	for i in range(24):
		tr2.append(p2[i + 24] + tr2[i])

	for i in range(48):
		res.append([st + "#" + str(i), tr0[i], tr1[i], tr2[i]])

with open("../res/submit.csv", "w", newline = "") as f:
    writer = csv.writer(f)
    for row in res:
        writer.writerow(row)
