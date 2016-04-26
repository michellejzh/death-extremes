import csv
import geocoder
import os
import sys
import sets


def createDataset(policefile, weatherfile, zipfile, gasfile):
	# SAVE EVERYTHING INTO DICTIONARIES AND THEN ACCESS BY DATE
	pass


def saveWeather(weatherfile):
	# open the weather data
	weather = open(weatherfile, "rU")
	weatherReader  = csv.DictReader(weather) 
	weatherDict = {} # date, maxtemp, mintemp, precipitation
	averageDict = {}
	yesterDict = {}

	qPrcp = []
	qSnow = []
	qTmax = []
	qTmin = []
	qAwnd = []
	count = 0
	for row in weatherReader:
		count += 1
		qPrcp.insert(0, float(row['PRCP']))
		qSnow.insert(0, float(row['SNOW']))
		qTmax.insert(0, float(row['TMAX']))
		qTmin.insert(0, float(row['TMIN']))
		qAwnd.insert(0, float(row['AWND']))

		if count < 7:
			yPrcp = row['PRCP']
			ySnow = row['SNOW']
			yTmax = row['TMAX']
			yTmin = row['TMIN']
			yAwnd = row['AWND']

		else:
			qPrcp.pop()
			qSnow.pop()
			qTmax.pop()
			qTmin.pop()
			qAwnd.pop()

			avgPrcp = 0
			avgSnow = 0
			avgTmax = 0
			avgTmin = 0
			avgAwnd = 0

			# calculate the moving average of each of these values for the last week
			for x in list(qPrcp):
				avgPrcp += x
			avgPrcp = float(avgPrcp)/7.0

			for x in list(qSnow):
				avgSnow += x
			avgSnow = float(avgSnow)/7.0

			for x in list(qTmax):
				avgTmax += x
			avgTmax = float(avgTmax)/7.0

			for x in list(qTmin):
				avgTmin += x
			avgTmin = float(avgTmin)/7.0

			for x in list(qAwnd):
				avgAwnd += x
			avgAwnd = float(avgAwnd)/7.0

			# PRCP, SNOW, TMAX, TMIN, AWND
			weatherDict[row['DATE']] = [row['PRCP'], row['SNOW'], row['TMAX'], row['TMIN'], row['AWND']]
			averageDict[row['DATE']] = [avgPrcp, avgSnow, avgTmax, avgTmin, avgAwnd]
			yesterDict[row['DATE']] = [yPrcp, ySnow, yTmax, yTmin, yAwnd]

			# save as yesterday
			yPrcp = row['PRCP']
			ySnow = row['SNOW']
			yTmax = row['TMAX']
			yTmin = row['TMIN']
			yAwnd = row['AWND']


	# print "========================================="
	# print yesterDict
	# print "========================================="
	# sys.exit()
	return weatherDict, averageDict, yesterDict

def checkIncomeBracket(income):
	# TODO: check which
	income = float(income) 
	if income<=29044:
		return 0
	elif income<=34374:
		return 1
	elif income<=35637:
		return 2
	elif income<=47086:
		return 3
	elif income<=63549:
		return 4
	else:
		return 5


def mergeZipcodeInfoWithWeather(zipcodefile, weatherDict, averageDict, yesterDict):
	allDates = {}
	zips = open(zipcodefile, "rU")
	zipsReader  = csv.DictReader(zips)
	zip_income = {}
	for row in zipsReader:
		bracket = checkIncomeBracket(row['Average Income'])
		if row['Date'] in allDates:
			allDates[row['Date']][bracket] += 1
		else:
			allDates[row['Date']] = {}
			for i in xrange(6):
				allDates[row['Date']][i] = 0
			allDates[row['Date']][bracket] = 1


	print allDates

	writePath = "full_dataset.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		weatherTitles = ["Precipitation", "Snow", "Tmax", "Tmin", "Awnd", "Avg Precipitation", "Avg Snow", "Avg Tmax", "Avg Tmin", "Avg Awnd", "Yester Precipitation", "Yester Snow", "Yester Tmax", "Yester Tmin", "Yester Awnd"]
		writer.writerow(["Date", "Emergencies", "income0", "income1", "income2", "income3", "income4", "income5"] + weatherTitles)
		# writer.writerow(["Id", "Zipcode", "Average Income", "Date", "income0", "income1", "income2", "income3", "income4", "income5"] + weatherTitles)

		zips = open(zipcodefile, "rU")
		zipsReader  = csv.DictReader(zips)
		zip_income = {}

		print weatherDict
		observedDates = sets.Set()
		for row in zipsReader:
			if row["Date"] in observedDates:
				pass
			else:
				observedDates.add(row["Date"])
				try:
					for i in xrange(6): # for each of 6 income brackets
						old = [row["Date"]]
						emergencies = allDates[row['Date']][i]
						incomes = [emergencies]
						for b in xrange(6):
							if b==i:
								incomes.append(1)
							else:
								incomes.append(0)
						# incomes = [allDates[row['Date']][0], allDates[row['Date']][1], allDates[row['Date']][2], allDates[row['Date']][3], allDates[row['Date']][4], allDates[row['Date']][5]]
						weather = weatherDict[row["Date"]] + averageDict[row["Date"]] + yesterDict[row["Date"]]
						print old
						print weather
						writer.writerow(old + incomes + weather)
				except KeyError, e:
					print "KeyError: " + str(e)


def savePolice(policefile):
	# open the 911 data
	police = open(policefile, "rU")
	policeReader  = csv.DictReader(police) 
	policeDict = {}
	for row in policeReader:
		wholeDate = row['FROMDATE']
		wholeDate = wholeDate.split(' ')
		mdy = wholeDate[0]
		time = wholeDate[1]

		# count the number of medical calls for each date that appears
		# ***BIG QUESTION: HOW TO MAKE DUMMIES TO SEE VARIABLE EFFECT BY INCOME?***
		pass

def saveZipcodes(policefile, incomesfile):
	# get the zipcodes of each location that shows up in the police data with
	# reverse geocoding from the python package (this will take a while)
	# then look up the associated average income
	incomes = open(incomesfile, "rU")
	incomeReader  = csv.DictReader(incomes)
	zip_income = {}
	for row in incomeReader:
		zipcode = "0" + str(row["Zip code"])
		income2005 = row["Average income, 2005"]
		zip_income[zipcode] = income2005

	writePath = "zipcode-income.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["Id", "Zipcode", "Average Income", "Date", "Time", "NatureCode"])

		police = open(policefile, "rU")
		policeReader  = csv.DictReader(police) 
		zipDict = {} # date, maxtemp, mintemp, precipitation 
		for row in policeReader:
			if row['INCIDENT_TYPE_DESCRIPTION']!="MedAssist":
				pass
			else: 
				location = row['Location']
				location = (location[1:(len(location)-1)]).split(', ')
				lat = location[0]
				lon = location[1]

				# get the time-date info
				timestamp = row["FROMDATE"].split(' ')
				date = timestamp[0].split('/')
				year = "20" + str(date[2])
				month = str(date[0])
				if len(month) < 2:
					month = "0" + str(month)
				day = str(date[1])
				if len(day) < 2:
					day = "0" + str(day)
				date = year + month + day
				print "DATE: " + str(date)
				# see file 1
				if date < "20121114":
					print "in earlier file..."
					pass
				else:
					time = timestamp[1]
					if len(time) < 5:
						time = "0" + str(time)
					print "TIME: " + str(time)

					# attempt to geocode
					g = geocoder.google([lat,lon], method='reverse')
					try:
						zipcode = (str(g.json['postal']).split("'"))[0]
						writer.writerow([row['COMPNOS'], zipcode, zip_income[zipcode], date, time, row["NatureCode"]])
					except KeyError, e:
						print "------KeyError: " + str(e) + str("------")


def saveGasPrice():
	# get price of natural gas that day. this is probably something that should
	# be averaged over some time
	gas = open(gasfile, "rU")
	gasReader  = csv.DictReader(gas)
	gasDict = {} # date, maxtemp, mintemp, precipitation, 
	for row in gasReader:
		# save each date in gas dict
		pass






if __name__ == '__main__':
	# saveZipcodes('Crime_Incident_Reports.csv', 'boston_income.csv')
	weatherDict, averageDict, yesterDict = saveWeather('boston_climate_data.csv')
	mergeZipcodeInfoWithWeather('zipcode-income_MERGE.csv', weatherDict, averageDict, yesterDict)

