import pickle
import numpy
import time
from sklearn.linear_model import LinearRegression

london_stations = {'BL0':0, 'CD1':1, 'CD9':2, 'GN0':3, 'GN3':4, 'GR4':5, 'GR9':6, 'HV1':7, 'KF1':8, 'LW2':9,
                   'ST5':10, 'TH4':11, 'MY7':12}

def getCoef(idx):
    py = dat[idx]
    linear = LinearRegression()
    linear.fit(px, py)
    res.append(linear.coef_)
    res.append(linear.intercept_)

if __name__ == "__main__":
    with open("../data/london_data.pkl", "rb") as f:
        dat = pickle.load(f)
    l = len(dat[0])
    tpx = [];
    for i in range(l):
        tpx.append([])
        for j in range(861):
            tpx[i].append(dat[72 + j * 5][i])
            tpx[i].append(dat[72 + j * 5 + 1][i])
            tpx[i].append(dat[72 + j * 5 + 2][i])
            tpx[i].append(dat[72 + j * 5 + 4][i])
    px = numpy.array(tpx).reshape(-1, 861 * 4)

    print("grid data initialized.")    

    res = []

    for st in aqstations:
        getCoef(aqstations[st] * 6)
        getCoef(aqstations[st] * 6 + 1)

    with open("../data/ldols_res.pkl", "wb") as f:
        pickle.dump(res, f)
