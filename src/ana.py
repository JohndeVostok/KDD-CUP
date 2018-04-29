import pickle
#from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

if __name__ == "__main__":
	aqData = {}
	with open("aqData.pkl", "rb") as f:
		aqData = pickle.load(f)

	l = aqData["stationData"]["aotizhongxin_aq"]

	datlist = []
	for i in l:
		try:
			datlist.append(float(i["pm25"]))
		except:
			datlist.append(0)
	dat = np.array(datlist)
	dat = dat.reshape(-1, 1)

	a = dat[-48:]
	dat = dat[:-48]
	with open("tmp.pkl", "wb") as f:
		pickle.dump(dat, f)
