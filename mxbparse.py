#!/usr/bin/python3

# wxbparse.py
# Johnathan Gilman (robotfactory)
# robotshoelaces@gmail.com
# 2/17/19
#
# A tool for taking plain text from Weather Battle and putting it into something useful to a computer
# Copy/Paste the entire page from a battle page into a text file
# Then run that text file through this script
# Script will export csv or json files
#
# Imports are:
# re for regular expressions
# csv to write to a csv
# hashlib to create the battle hash
# json to export json
# argparse to parse artuments

import re, csv, hashlib, json, argparse

parser = argparse.ArgumentParser(description='Injests plain text from WXBattle and spits out pretty stuff')
parser.add_argument('input_file', help='The file to injest')
parser.add_argument('-f', '--format', help='Output to csv or json. (Default: csv)', required=False)
args = parser.parse_args()

if args.format:
	if ("csv" not in args.format) and ("json" not in args.format):
		raise Exception('Invalid output format')

# Use the positional argument to get the input file
if args.input_file:
	input_filename = args.input_file
else:
	raise Exception("Must specify an input file")

# Open the input file and read it to an array
try:
	with open (input_filename) as file:
		file_array = file.readlines()
except:
	raise

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
	if ("Daily" in current_line) and ("Battle" in current_line) and ("(" in current_line) and (")" in current_line and (("Heat" in current_line) or ("Cold" in current_line) or ("Precip" in current_line) or ("Wind" in current_line))):
		# The battle title looks like 'Daily Battle $5 (Heat)'
		battle_data['metadata']['battle_title'] = current_line.strip()
		# Battle format is Heat, Cold, Wind, Precip, etc.
		battle_data['metadata']['battle_format'] = re.search(r"(?<=\().+?(?=\))",current_line).group(0)

	# Look for the lines with the points available in this battle
	if ("Points Remaining" in current_line):
		# The points are on the next line
		battle_data['metadata']['points_available'] = int(next_line)

	# Look for the line with the rest of the metadata
	if ("Begins" in current_line) and ("Prize" in current_line) and ("Entry" in current_line) and ("Closes" in current_line):
		battle_data['metadata']['begins'] = re.search(r"((Begins: )(.*?)( EST))",current_line).group(3).strip()
		battle_data['metadata']['prize'] = re.search(r"((Prize: \$)(.*?)(WBP))",current_line).group(3).strip()
		battle_data['metadata']['wbp'] = re.search(r"((WBP: )(.*?)(Entry))",current_line).group(3).strip()
		battle_data['metadata']['entry_fee'] = re.search(r"((Entry Fee: \$)(.*?)(Entry Type))",current_line).group(3).strip()
		# So far we'v eonly seen entry_type = 'Single Entry'
		battle_data['metadata']['entry_type'] = re.search(r"((Entry Type: )(.*?)(Battle Type))",current_line).group(3).strip()
		# Currently only one battle type is available and that's 'Daily'
		battle_data['metadata']['battle_type'] = re.search(r"((Battle Type: )(.*?)(Closes))",current_line).group(3).strip()

	# Increment the line number so we move on
	line_number += 1

# We don't need the array we stored all the lines in anymore
del(file_array)

print("Processing " + battle_data['metadata']['battle_title'])

print ("Generating Battle Hash")
# Use the new dictionary object to create a hash to identify the battle
battle_data_str = json.dumps(battle_data)
battle_hash = hashlib.sha256(battle_data_str.encode()).hexdigest()

# Sort stuff from highest cost to lowest
sorted_cities = sorted(battle_data['cities'], key = lambda i: i['points'], reverse=True)

# Print some info so you can tell the script is actually doing something
print("Begins: " + battle_data['metadata']['begins'])
print("Cities Found: " + str(len(battle_data['cities'])))
print("Battle Hash (SHA256): " + str(battle_hash))
print("Writing to file ...")

# Do JSON stuff
if ("json" in args.format):
	# Build the name of the file we're writing to
	output_filename = battle_data['metadata']['battle_type'] + "-" + battle_data['metadata']['battle_format'] + "-" + battle_data['metadata']['begins'].split(",")[0].strip().replace(" ","") + ".json"
	print(output_filename)
	with open(output_filename, 'w') as outfile:
		json.dump(battle_data, outfile)

# Do CSV Stuff
else:
	# Build the name of the file we're writing to
	output_filename = battle_data['metadata']['battle_type'] + "-" + battle_data['metadata']['battle_format'] + "-" + battle_data['metadata']['begins'].split(",")[0].strip().replace(" ","") + ".csv"
	print(output_filename)
	# Define the keys, or column names
	keys = sorted_cities[0].keys()

	# Write stuff to the file
	with open(output_filename, 'w') as output_file:
		# First write the comments to the top of the file
		output_file.write("# " + battle_data['metadata']['battle_title'] + "\n")
		output_file.write("# Battle Begins: " + battle_data['metadata']['begins'] + "\n")
		output_file.write("# Entry Fee: $" + battle_data['metadata']['entry_fee'] + "\n")
		output_file.write("# Battle Hash: " + str(battle_hash) + "\n")
		# Set the output file for DictWriter and set the header row
		dict_writer = csv.DictWriter(output_file, fieldnames=keys)
		# Write the header row
		dict_writer.writeheader()
		# Write the rest of the lines
		dict_writer.writerows(sorted_cities)

print("Done!")
