import requests
import sys

if __name__ == "__main__":
	filename = "../data/tmpres.csv"
	files = {
		'files': open(filename, 'rb')
	}
	data = {
		"user_id": "JDVostok",
		"team_token": "b976f11c7e36a211a03c8d46a74b9d8432c0e62673ce366ac5fdd93a206b7014",
		"description": filename,
		"filename": filename,
	}
	url = 'https://biendata.com/competition/kdd_2018_submit/'
	response = requests.post(url, files=files, data=data)
	print(response.text)
