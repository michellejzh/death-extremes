import csv

def printAsJSVar(filename):
	print "var coordinates = ["
	fileReader = open(filename, "rU")
	reader  = csv.DictReader(fileReader) 
	for row in reader:
		# print row
		rowID = row["Compnos"]
		coords = str(row["Location"])
		# lon = coords[0]
		# lat = coords[1]
		coordLen = len(coords)
		coords = coords[1:coordLen-1]
		# print coords
		# skip the rows with invalid coordinates or ID
		if coords == "0.0, 0.0":
			pass
		elif rowID == '':
			pass
		else:
			print '{"id": ' + str(rowID) + ', "coordinates": [' + str(coords) + ']},'
	print "]"




if __name__ == '__main__':
	printAsJSVar("coordinates.csv")

