import pickle
import numpy
import time
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        dat = pickle.load(f)
    l = len(dat[0])
    tpx = [];
    for i in range(l):
        if i % 1000 == 0:
            print(str(i)+'/'+str(l))
        tpx.append([])
        for j in range(651):
            tpx[i].append(dat[300 + j * 5][i])
            tpx[i].append(dat[300 + j * 5 + 1][i])
            tpx[i].append(dat[300 + j * 5 + 2][i])
            tpx[i].append(dat[300 + j * 5 + 4][i])
    px = numpy.array(tpx).reshape(-1, 651 * 4)
    print(px.shape)
    py = dat[0]
    linear = LinearRegression()
    linear.fit(px, py)
    print(linear.coef_)
	
