import csv
import geocoder
import os
import sys
import sets

def getDailyWeather():
	weatherfile = 'boston_climate_data.csv'
	weather = open(weatherfile, "rU")
	weatherReader  = csv.DictReader(weather) 
	tmaxDict = {}

	for row in weatherReader:
		tmaxDict[row['DATE'][4:]] = float(row['TMAX'])
	return tmaxDict

def tempsByCode():
	tmaxDict = getDailyWeather()
	allDates = {}
	zipcodefile = 'zipcode-income_MERGE.csv'
	zips = open(zipcodefile, "rU")
	zipsReader  = csv.DictReader(zips)
	zip_income = {}
	for row in zipsReader:
		nature = row["NatureCode"]
		print "Before: " + nature
		print nature == "CARST "
		if nature == "CARDIA" or nature == "CARST " or nature == "UNCONS" or nature == "IVPER" or nature == "UNK":
			print "After: " + nature
			if row['Date'] in allDates:
				# print "ALREADY EXISTS"
				allDates[row['Date']][nature] += 1
			else:
				allDates[row['Date']] = {}
				allDates[row['Date']]["CARDIA"] = 0
				allDates[row['Date']]["CARST "] = 0
				allDates[row['Date']]["UNCONS"] = 0
				allDates[row['Date']]["IVPER"] = 0
				allDates[row['Date']]["UNK"] = 0
				allDates[row['Date']][nature] = 1
	# print allDates
	writePath = "tempsByCode.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["Date", "TMax", "CARDIA", "CARST", "UNCONS", "IVPER", "UNK"])
		for date in allDates:
			writer.writerow([date, tmaxDict[date[4:]], allDates[date]["CARDIA"], allDates[date]["CARST "], allDates[date]["UNCONS"], allDates[date]["IVPER"], allDates[date]["UNK"]])



if __name__ == '__main__':
	tempsByCode()