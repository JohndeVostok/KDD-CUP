import pickle
import numpy

if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        data = pickle.load(f)
    n = data.shape[0]
    l = data.shape[1]

    for idx in range(n):
        numl = numpy.zeros(24, dtype = float)
        suml = numpy.zeros(24, dtype = float)
        for t in range(l):
            if (data[idx][t] != 0):
                numl[t % 24] += 1
                suml[t % 24] += data[idx][t]
        for t in range(l):
            if (data[idx][t] == 0):
                data[idx][t] = suml[t % 24] / numl[t % 24]
        if idx % 100 == 0:
            print(idx)
    with open("../data/bj_clean.pkl", "wb") as f:
        pickle.dump(data, f)

    with open("../data/london_data.pkl", "rb") as f:
        data = pickle.load(f)
    n = data.shape[0]
    l = data.shape[1]

    for idx in range(n):
        numl = numpy.zeros(24, dtype = float)
        suml = numpy.zeros(24, dtype = float)
        for t in range(l):
            if (data[idx][t] != 0):
                numl[t % 24] += 1
                suml[t % 24] += data[idx][t]
        for t in range(l):
            if (data[idx][t] == 0):
                data[idx][t] = suml[t % 24] / numl[t % 24]
        if idx % 100 == 0:
            print(idx)
    with open("../data/ld_clean.pkl", "wb") as f:
        pickle.dump(data, f)
    
