#!/usr/bin/python3

# wxbparse.py
# Johnathan Gilman (robotfactory)
# robotshoelaces@gmail.com
# 2/17/19
#
# A tool for taking plain text from Weather Battle and putting it into something useful to a computer
# Copy/Paste the entire page from a battle page into a text file
# 
#
# Imports are:
# re for regular expressions
# json to export json

import re, json
from datetime import datetime

# Open the input file and read it to an array

def wxbparse(file_array):
	# Function should recieve an array of lines from the input file

	# Init a pretty named dict to put all the battle data in
	battle_data = {}
	# Put the metadata and city data inside the pretty dict
	battle_data['metadata'] = {}
	battle_data['cities'] = []

	# Regex to use later to find numbers inside of strings with other stuff
	numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
	rx = re.compile(numeric_const_pattern, re.VERBOSE)

	# Set the line number where we begin. The first line is a good place to start.
	line_number = 0

	# Loop through the array created from the file and search for stuff
	while line_number < len(file_array):
		# Store the current line to a str
		current_line = file_array[line_number].strip()

		# Do this until the line before last
		if line_number < len(file_array)-1:
			next_line = file_array[line_number + 1].strip()
		# Since there's no next line after the last line set next_line to None
		else:
			next_line = None

		# Look for the line with the city name and airport code
		if ("," in current_line) and ("(" in current_line) and ("$" not in current_line):
			# Create a new named dictionary to put this city's info in
			city_info = {}
			# Get the City Name
			city_info['city'] = re.search(r"([A-Za-z]+(?: [A-Za-z]+)*),? ([A-Za-z]{2})",current_line).group(0)
			# Get the Airport Code
			city_info['airport']=re.search(r"(?<=\().+?(?=\))",current_line).group(0).strip()
			# Get the Forecast, historical (normal, 7 day average, etc), and Points. These numbers are on the next line
			numbers=rx.findall(next_line)
			# Save the forecasted number
			city_info['forecast'] = float(numbers[0])
			# Here, 'normal' means whatever historical number WXB is giving us (normal, 7 day avg, etc)
			city_info['historical'] = float(numbers[1])
			# Save the points number
			city_info['points'] = float(numbers[2])
			# Stuff the new city's info into a list of other cities' stuff
			battle_data['cities'].append(city_info)
			# We don't need this dict anymore
			del(city_info)

		# Look for the line with the battle title and format
		if (("Rapid" in current_line or "Daily" in current_line or "24 Hour" in current_line) and ("Battle" in current_line) and (("Heat" in current_line) or ("Cold" in current_line) or ("Precip" in current_line) or ("Wind" in current_line))) or ("Head To Head" in current_line):
			# The battle title looks like 'Daily Battle $5 (Heat)'
			battle_data['metadata']['battle_title'] = current_line.strip()
			# Battle format is Heat, Cold, Wind, Precip, etc.
			if ("hottest" in next_line):
				battle_data['metadata']['battle_format'] = "Heat"
			elif ("coldest" in next_line):
				battle_data['metadata']['battle_format'] = "Cold"
			elif ("windiest" in next_line):
				battle_data['metadata']['battle_format'] = "Wind"
			elif ("wettest" in next_line) or ("Precip" in current_line):
				battle_data['metadata']['battle_format'] = "Precip"
			else:
				raise Exception("Invalid battle format found")

		# Look for the lines with the points available in this battle
		if ("Points Remaining" in current_line):
			# The points are on the next line
			battle_data['metadata']['points_available'] = int(next_line)

		# Look for the line with how many cities you can select
		if ("Selected Cities" in current_line):
			# Try to get the number after the slash
			battle_data['metadata']['max_cities'] = current_line.split(" / ")[1]

		# Look for the line with the rest of the metadata
		if ("Begins" in current_line) and ("Prize" in current_line) and ("Entry" in current_line) and ("Closes" in current_line):
			# WXB displays the start and end time and date weird. Split it up, add a year so datetime doesn't barf.
			# TODO: This is going to break if it's Dec 31 and you're running for a battle starting on Jan 1
			start_time = re.sub("st|nd|rd|th","",re.search(r"((Begins: )(.*?)(Ends:))",current_line).group(3).strip())
			battle_data['metadata']['begins'] = start_time.split(", ")[0] + ", " + str(datetime.today().year) + " " + start_time.split(", ")[1]
			end_time = re.sub("st|nd|rd|th","",re.search(r"((Ends: )(.*?)(Prize:))",current_line).group(3).strip())
			battle_data['metadata']['ends'] = end_time.split(", ")[0] + ", " + str(datetime.today().year) + " " + end_time.split(", ")[1]
			
			battle_data['metadata']['prize'] = re.search(r"((Prize: \$)(.*?)(Entry Fee))",current_line).group(3).strip()
			# WBP (weather battle points) showed up for a while and then disappeared. Future implementation?
			# battle_data['metadata']['wbp'] = re.search(r"((WBP: )(.*?)(Entry))",current_line).group(3).strip()
			battle_data['metadata']['entry_fee'] = re.search(r"((Entry Fee: \$)(.*?)(Entry Type))",current_line).group(3).strip()
			battle_data['metadata']['entry_type'] = re.search(r"((Entry Type: )(.*?)(Battle Type))",current_line).group(3).strip()
			# Battle type is daily, rapid, etc
			battle_data['metadata']['battle_type'] = re.search(r"((Battle Type: )(.*?)(Closes))",current_line).group(3).strip()

		# Increment the line number so we move on
		line_number += 1

	# We don't need the array we stored all the lines in anymore
	del(file_array)
	
	# Return our pretty dictionary object
	return(battle_data)