import pickle
import numpy
import time
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import matplotlib.pyplot as plt

if __name__ == "__main__":
	with open("tmp.pkl", "rb") as f:
		dat = pickle.load(f)
		
	print(len(dat))

	d = 24
	td = []
	l = len(dat)
	for i in range(d, l):
		td.append(dat[i] - dat[i - d])
	dat = numpy.array(td)

	'''
	fig = plt.figure(figsize=(12,8))
	ax1=fig.add_subplot(211)
	fig = sm.graphics.tsa.plot_acf(dat,lags=40,ax=ax1)
	ax2 = fig.add_subplot(212)
	fig = sm.graphics.tsa.plot_pacf(dat,lags=40,ax=ax2)	
	fig.savefig("plt.png")
	'''

	datarma = sm.tsa.ARMA(dat,(18,3)).fit()

	res = datarma.predict(10250, 10298, dynamic = True)
	
	print(res)
	
	b = []
	for i in range(24):
		b.append(res[i] + dat[i - 24])
	for i in range(24):
		b.append(res[i + 24] + b[i])
	
	print(b)
	'''
	
	p = 72
	l = len(dat)
	py = dat[p:].reshape(-1, 1)
	tpx = [];
	for i in range(l - p):
		tpx.append(dat[i:i + p])
	
	px = numpy.array(tpx).reshape(-1, p)
	print(px.shape)

	linear = LinearRegression()
	linear.fit(px, py)
	
	print(linear.coef_)
	'''
