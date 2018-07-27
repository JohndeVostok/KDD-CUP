import pickle
import numpy
if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        data = pickle.load(f)
        n = data.shape[0]
        l = data.shape[1]

    meo = numpy.zeros((l, 4))
    for i in range(l):
        s = [0, 0, 0, 0]
        t = [0, 0, 0, 0]
        for j in range(651):
            tmp = data[300 + j * 5 + 0][i]
            if tmp != 0:
                s[0] += tmp
                t[0] += 1
            tmp = data[300 + j * 5 + 1][i]
            if tmp != 0:
                s[1] += tmp
                t[1] += 1
            tmp = data[300 + j * 5 + 2][i]
            if tmp != 0:
                s[2] += tmp
                t[2] += 1
            tmp = data[300 + j * 5 + 4][i]
            if tmp != 0:
                s[3] += tmp
                t[3] += 1
        for j in range(4):
            if t[j] != 0:
                meo[i][j] = s[j] / t[j]
        if i % 1000 == 0:
            print(i)
    with open("../data/meoaverage.pkl", "wb") as f:
        pickle.dump(meo, f)
