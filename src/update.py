from datetime import datetime
from datetime import timedelta
import requests
import pickle
import csv

if __name__ == "__main__":
	aqData = {}
	with open("aqData.pkl", "rb") as f:
		aqData = pickle.load(f)

	endTime = datetime.strptime(aqData["endTime"], "%Y-%m-%d %H:%M:%S")
	nowTime = datetime.now()
	nowTime = datetime(nowTime.year, nowTime.month, nowTime.day, nowTime.hour)
	urlPre = "http://biendata.com/competition/airquality/bj/"
	urlSuf = "/2k0d1d8"
	url = urlPre + endTime.strftime("%Y-%m-%d-%H") + "/" + nowTime.strftime("%Y-%m-%d-%H") + urlSuf

	response = requests.get(url)
	dataList = response.text.split("\r\n")
	tmpData = []
	for entry in dataList:
		tmpData.append(entry.split(","))

	tmpData.pop(0)
	for entry in tmpData:
		aqData["stationData"][entry[1]].append({"time": entry[2], "pm25": entry[3], "pm10": entry[3], "o3": entry[7]})

	with open("aqData.pkl", "wb") as f:
		pickle.dump(aqData, f)
