import pickle
import numpy
import time
import math
from sklearn.linear_model import LinearRegression

aqstations = {'BL0':0, 'CD1':1, 'CD9':2, 'GN0':3, 'GN3':4, 'GR4':5, 'GR9':6, 'HV1':7, 'KF1':8, 'LW2':9,
                   'ST5':10, 'TH4':11, 'MY7':12}

ngrid = 861

def getCoef(idx):
	py = tmpdata[24:]
	linear = LinearRegression()
	linear.fit(px, py)
	res.append([linear.coef_, linear.intercept_])

if __name__ == "__main__":
    with open("../data/london_data.pkl", "rb") as f:
        dat = pickle.load(f)
    l = len(dat[0])

	px = numpy.zeros(((l - 48), (ngrid * 4 + 19)), dtype = numpy.float32)
	for i in range(48, l):
		for j in range(ngrid):
			px[i - 48][j * 4] = dat[72 + j * 5][i - 24]
			px[i - 48][j * 4 + 1] = dat[72 + j * 5 + 1][i - 24]
			px[i - 48][j * 4 + 2] = dat[72 + j * 5 + 2][i - 24]
			px[i - 48][j * 4 + 3] = dat[72 + j * 5 + 4][i - 24]


	res = []
	for st in aqstations:
		print(st)
		print("PM2.5")
		idx = aqstations[st] * 3 + 0
		tmpdata = numpy.zeros(l - 24)
		for i in range(24, l):
			tmpdata[i - 24] = dat[idx][i] - dat[idx][i - 24]
		for i in range(48, l):
			px[i - 48][ngrid * 4] = math.sin(i / 12 * math.pi)
			for j in range(1, 19):
				px[i - 48][ngrid * 4 + j] = tmpdata[i - 24 - j]
		getCoef(idx)

		print("PM10")
		idx = aqstations[st] * 3 + 1
		tmpdata = numpy.zeros(l - 24)
		for i in range(24, l):
			tmpdata[i - 24] = dat[idx][i] - dat[idx][i - 24]

		for i in range(48, l):
			px[i - 48][ngrid * 4] = math.sin(i / 12 * math.pi)
			for j in range(1, 19):
				px[i - 48][ngrid * 4 + j] = tmpdata[i - 24 - j]
		getCoef(idx)

    with open("../data/ldols_res.pkl", "wb") as f:
        pickle.dump(res, f)
