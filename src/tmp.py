import pickle
import numpy
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
	with open("tmp.pkl", "rb") as f:
		dat = pickle.load(f)
	
	d = 24
	td = []
	l = len(dat)
	for i in range(d, l):
		td.append(dat[i] - dat[i - d])
	dat = numpy.array(td)
	
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
