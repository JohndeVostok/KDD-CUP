import csv
import numpy
import pickle

with open("../pkl/beijing_data.pkl", "rb") as f:
    data = pickle.load(f)

res = [["test_id", "PM2.5", "PM10", "O3"], ["dongsi_aq#" + str(1), 0, 0, 0]]

with open("../res/submit.csv", "w", newline = "") as f:
    writer = csv.writer(f)
    for row in res:
        writer.writerow(row)
