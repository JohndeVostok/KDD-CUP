import pickle
import csv

if __name__ == "__main__":
	filename = "../data/beijing_17_18_aq.csv"
	data = []
	with open(filename, "r") as f:
		reader = csv.reader(f)
		data = list(reader)
	data.pop(0)
	aqData = {}
	aqData["startTime"] = "2017-01-01 14:00:00"

	aqData["stationData"] = {}

	for entry in data:
		if not entry[0] in aqData["stationData"]:
			aqData["stationData"][entry[0]] = [];
		aqData["stationData"][entry[0]].append({"time": entry[1], "pm25": entry[2], "pm10": entry[3], "o3": entry[6]})

	filename = "../data/beijing_201802_201803_aq.csv"
	with open(filename, "r") as f:
		reader = csv.reader(f)
		data = list(reader)
	data.pop(0)
	for entry in data:
		if not entry[0] in aqData["stationData"]:
			aqData["stationData"][entry[0]] = [];
		aqData["stationData"][entry[0]].append({"time": entry[1], "pm25": entry[2], "pm10": entry[3], "o3": entry[6]})

	with open("aqData.pkl", "wb") as f:
		pickle.dump(aqData, f)
