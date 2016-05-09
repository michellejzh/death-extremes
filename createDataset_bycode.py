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


def loadPopulations(popfile):
	pops = open(popfile, "rU")
	popsReader  = csv.DictReader(pops)
	populationBrackets = {}
	for i in xrange(6):
		populationBrackets[i] = 0

	for row in popsReader:
		code = str(row["Zip code"])
		inc = int(float(row["Average income, 2005"]))
		try:
			pop = int(float(row["Population 2013"]))
			bracket = checkIncomeBracket(inc)
			populationBrackets[bracket] = populationBrackets[bracket] + pop
		except ValueError:
			print "Error: " + str(code) + " is missing its population"
	return populationBrackets



def mergeZipcodeInfoWithWeather(zipcodefile, weatherDict, averageDict, yesterDict, zipSet):
	allDates = {}
	zips = open(zipcodefile, "rU")
	zipsReader  = csv.DictReader(zips)
	zip_income = {}
	for row in zipsReader:
		nature = row["NatureCode"]
		if nature != "CARDIA" and nature != "CARST" and nature != "UNCONS" and nature != "IVPER" and nature != "UNK":
			print "Not correct nature"
			pass
		else:
			bracket = checkIncomeBracket(row['Average Income'])
			if row['Date'] in allDates:
				allDates[row['Date']][bracket] += 1
			else:
				allDates[row['Date']] = {}
				for i in xrange(6):
					allDates[row['Date']][i] = 0
				allDates[row['Date']][bracket] = 1

	population = loadPopulations('zips_population.csv')
	writePath = "full_dataset_BYCODE.csv"
	lows, highs = loadHistAverages()
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		weatherTitles = ["Precipitation", "Snow", "Tmax", "Tmin", "Awnd", "Avg Precipitation", "Avg Snow", "Avg Tmax", "Avg Tmin", "Avg Awnd", "Yester Precipitation", "Yester Snow", "Yester Tmax", "Yester Tmin", "Yester Awnd", "Avg Low", "Avg High"]
		writer.writerow(["Date", "Emergencies", "Per Cap Emergencies", "income0", "income1", "income2", "income3", "income4", "income5"] + weatherTitles)
		# writer.writerow(["Id", "Zipcode", "Average Income", "Date", "income0", "income1", "income2", "income3", "income4", "income5"] + weatherTitles)

		zips = open(zipcodefile, "rU")
		zipsReader  = csv.DictReader(zips)
		zip_income = {}

		# print weatherDict
		observedDates = sets.Set()
		print zipSet
		rejectedZips = sets.Set()
		for row in zipsReader:
			# print row
			if str(row["Zipcode"]) in zipSet:
				if row["Date"] in observedDates:
					pass
				else:
					observedDates.add(row["Date"])
					try:
						for i in xrange(6): # for each of 6 income brackets
							old = [row["Date"]]
							emergencies = allDates[row['Date']][i]
							perCapEmergencies = float(emergencies)/float((population[i]))
							incomes = [emergencies] + [perCapEmergencies]
							for b in xrange(6):
								if b==i:
									incomes.append(1)
								else:
									incomes.append(0)
							# incomes = [allDates[row['Date']][0], allDates[row['Date']][1], allDates[row['Date']][2], allDates[row['Date']][3], allDates[row['Date']][4], allDates[row['Date']][5]]
							weather = weatherDict[row["Date"]] + averageDict[row["Date"]] + yesterDict[row["Date"]]
							weather = weather + [lows[row["Date"][4:]]] + [highs[row["Date"][4:]]]
							# print old
							# print weather
							writer.writerow(old + incomes + weather)
					except KeyError, e:
						print "KeyError: " + str(e)
			else:
				if row["Zipcode"] not in rejectedZips:
					rejectedZips.add(row["Zipcode"])
				# print str(row["Zipcode"]) + " not in zipSet, moving on..."
				pass
		# print rejectedZips


# def savePolice(policefile):
# 	# open the 911 data
# 	police = open(policefile, "rU")
# 	policeReader  = csv.DictReader(police) 
# 	policeDict = {}
# 	for row in policeReader:
# 		wholeDate = row['FROMDATE']
# 		wholeDate = wholeDate.split(' ')
# 		mdy = wholeDate[0]
# 		time = wholeDate[1]

# 		# count the number of medical calls for each date that appears
# 		# ***BIG QUESTION: HOW TO MAKE DUMMIES TO SEE VARIABLE EFFECT BY INCOME?***
# 		pass


# def saveGasPrice():
# 	# get price of natural gas that day. this is probably something that should
# 	# be averaged over some time
# 	gas = open(gasfile, "rU")
# 	gasReader  = csv.DictReader(gas)
# 	gasDict = {} # date, maxtemp, mintemp, precipitation, 
# 	for row in gasReader:
# 		# save each date in gas dict
# 		pass


def lessThanReturns(incomesFile):
	incomes = open(incomesFile, "rU")
	incomesReader  = csv.DictReader(incomes)
	zipSet = sets.Set()
	# print "Zip code\t# of returns"
	for row in incomesReader:
		returns = int(float(row["Number of returns, 2001"]))
		if returns > 1000:
			code = str(row["Zip code"])
			# print code + "\t" + str(returns)
			if not code in zipSet:
				zipSet.add(code)
	return zipSet

def findUsedZips(zipcodefile):
	zipSet = sets.Set()
	zips = open(zipcodefile, "rU")
	zipsReader  = csv.DictReader(zips)
	for row in zipsReader:
		code = row["Zipcode"]
		if code not in zipSet:
			zipSet.add(code)
	stuff = [a for a in zipSet]
	stuff.sort()
	for thing in stuff:
		print thing

def loadHistAverages():
	filename = "historical_avg_temps.csv"
	lows = {}
	highs = {}
	hists = open(filename, "rU")
	histsReader  = csv.DictReader(hists)
	for row in histsReader:
		lows[row["Date"][4:]] = row["Average Low"]
		highs[row["Date"][4:]] = row["Average High"]
	return lows, highs

if __name__ == '__main__':
	# saveZipcodes('Crime_Incident_Reports.csv', 'boston_income.csv')
	# findUsedZips('zipcode-income_MERGE.csv')

	zipSet = lessThanReturns("boston_income.csv")
	weatherDict, averageDict, yesterDict = saveWeather('boston_climate_data.csv')
	mergeZipcodeInfoWithWeather('zipcode-income_MERGE.csv', weatherDict, averageDict, yesterDict, zipSet)

	

