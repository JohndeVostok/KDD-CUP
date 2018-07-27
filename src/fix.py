import pickle

def getBox(idx):
    tmp = [[] for i in range(24)]
    for i, x in enumerate(data[idx]):
        if (x != 0):
            tmp[i % 24].append(x)
    ans = [[] for i in range(24)]
    for i in range(24):
        tmp[i].sort()
        q1 = tmp[i][int(len(tmp[i]) / 4)]
        q3 = tmp[i][int(len(tmp[i]) * 3 / 4)]
        iqr = q3 - q1
        mn = max([min(tmp[i]), q1 - 1.5 * iqr])
        mx = min([max(tmp[i]), q3 + 1.5 * iqr])
        ans[i] = [mn, mx, q1, q3]
    res.append(ans)
        
if __name__ == "__main__":
    with open("../data/beijing_data.pkl", "rb") as f:
        data = pickle.load(f)
    res = []
    for i in range(35):
        getBox(i * 6 + 0)
        getBox(i * 6 + 1)
        getBox(i * 6 + 4)
    with open("../data/bj_box.pkl", "wb") as f:
        pickle.dump(res, f)

    with open("../data/london_data.pkl", "rb") as f:
        data = pickle.load(f)
    res = []
    for i in range(13):
        getBox(i * 3 + 0)
        getBox(i * 3 + 1)
    with open("../data/ld_box.pkl", "wb") as f:
        pickle.dump(res, f)
