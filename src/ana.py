import pickle
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
	aqData = {}
	with open("aqData.pkl", "rb") as f:
		aqData = pickle.load(f)

	l = aqData["stationData"]["aotizhongxin_aq"]

	dat = []
	for i in l:
		dat.append(i["pm25"])

	dx = range(len(dat))
	dy = dat

	dat0 = dat[:-1]
	dat1 = dat[1:]

	linreg = LinearRegression()
	linreg.fit(dat0,dat1)
	print(linreg.coef_)
	
	
	
