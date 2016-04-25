import csv
import geocoder
import os
import sys
import sets

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
				if date < "20130426":
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


if __name__ == '__main__':
	saveZipcodes('Crime_Incident_Reports.csv', 'boston_income.csv')