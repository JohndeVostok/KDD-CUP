import pickle

from keras.models import load_model

if __name__ == "__main__":
    with open("../data/netdata.pkl", "rb") as f:
        tmp = pickle.load(f)
    model = load_model("../data/model")
    trainx = tmp[0]
    trainy = tmp[1]
    testx = tmp[2]
    testy = tmp[3]

    y = model.predict(testx)
    tt = []
    for i in range(len(y)):
        s = 0
        for j in range(48):
            s += abs(y[i][j][0] - testy[i][j][0]) * 2 / (y[i][j][0] + testy[i][j][0])
        tt.append(s / 48)
    print(sum(tt) / len(tt))
