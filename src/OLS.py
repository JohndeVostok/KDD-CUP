import pickle
import numpy
import time
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import matplotlib.pyplot as plt

if __name__ == "__main__":
	with open("../data/beijing_data.pkl", "rb") as f:
		dat = pickle.load(f)
		
	l = len(dat[0])
	
	tpx = [];
	for i in range(l):
		tpx.append([])
		for j in range(651):
			tpx[i].append(dat[300 + j * 5])
			tpx[i].append(dat[300 + j * 5 + 1])
			tpx[i].append(dat[300 + j * 5 + 2])
			tpx[i].append(dat[300 + j * 5 + 4])
	
	px = numpy.array(tpx).reshape(-1, 4)
	print(px.shape)
	py = dat[0]

	linear = LinearRegression()
	linear.fit(px, py)
	
	print(linear.coef_)
	
