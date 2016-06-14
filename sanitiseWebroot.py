#!/usr/bin/python3
"""
	Sanitise date format for Webroot Secure Anywhere's export to CSV capabilities

	Original data format is not easily machine sortable
		example: "January 02 1970 12:22"

	Script rewrites datecolumns to:
		example: "1970-01-02 12:22"

	Author:		Andrew Waite <andrew.waite@infosanity.co.uk>
	Date:		2016-06-10
	Version:	v0.9
	License:	Beerware.....

	Thanks:		Mostly thanks to Al Sweigart's book "Automate the boring stuff with Python"
"""

import os	# File system management 
import sys 	# Commandline parameter handling and crash-on-failure logic
import re	# Regex for input validation
import csv	# Reading/writing CSV file format
import datetime	# Date format modifiation
import time	# NOT necessary, was playing at this point.....

def printHelp():
	return '''Script sanitises the date format from Webroot Secure Anywhere's "Export to CSV" output

script expects a single parameter, the filename of the original .csv file

script will create a single csv file with more sensible date format

USAGE:
	./sanitiseWebroot.py exportToCSV.csv'''

if ( ( len( sys.argv ) != 2 ) ):
	sys.exit ( printHelp() )

inputFile = sys.argv[1]

# Check Valid CSV file - Todo sanity check is Webroot output
csvRegex = re.compile(r'\w+.csv$')
if ( os.path.isfile( inputFile ) and csvRegex.search( inputFile ) ):
	
	# Open inport file
	print( "[*] Opening file: " + inputFile )

	exportFile = open( inputFile )
	exportReader = csv.reader(exportFile)
	exportData = list(exportReader)

	#Strip Header
	exportHeader = exportData[0]
	exportData = exportData[1:]

	# TO DO - Basic file format validation
	""" Assert statements not working as expected:.....
	
	assert exportHeader[0] == "Hostname", 'Unexpected file format: First column not "Hostname"'
	assert exportHeader[2] == 'First Seen', 'Unexpected file format: First column not "First Seen"'
	assert exportHeader[3] == 'Last Seen', 'Unexpected file format: First column not "Last Seen"'
	"""

	# Open output file
	inputSplit = inputFile.split( '.' )
	outputFile = inputSplit[0] + "-Sanitised." + inputSplit[1]

	if (os.path.isfile( outputFile ) ):
		sys.exit("Output file \"" + outputFile + "\" already exists; cowardly refusing to overwrite..... ")
	
	outputCSVobj = open(outputFile, 'w')
	csvWriter = csv.writer(outputCSVobj)
	
	# write Table Header to output file
	csvWriter.writerow(exportHeader)
	
	print("[*] Updating date fields....")
	numRows=0

	# Original Date format: "%B %d %Y %H %M" - Urgh!....
	webrootDateString = '%B %d %Y %H:%M'

	for row in exportData:

		# First Seen column
		row[2] = str( datetime.datetime.strptime( row[2], webrootDateString ) )

		# Last Seen column
		row[3] = str( datetime.datetime.strptime( row[3], webrootDateString ) )
		
		# write updated row record to output file
		csvWriter.writerow(row)
		
		numRows += 1
		if ( ( numRows % 100 ) == 0 ):
			print(str(numRows) + " records processed...")
			time.sleep(0.5) # unnecessary, but makes commandline output feel more interesting.....
	
	print("[*] Processing complete. " + str(numRows) + " corrected and written to " + outputFile)
else:
	sys.exit("Provided input file \"" + inputFile + "\" does not exist")

# Close files
outputCSVobj.close()
