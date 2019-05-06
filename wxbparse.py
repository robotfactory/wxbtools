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
# PrettyTable to make a pretty table
# argparse to parse arguments

import argparse, time
from wxbfunction import *
from nwsapi import *
from progressbar import *
from prettytable import PrettyTable


parser = argparse.ArgumentParser(description='Injests plain text from WXBattle and spits out pretty stuff')
parser.add_argument('input_file', help='The file to injest')
args = parser.parse_args()

# Use the positional argument to get the input file
if args.input_file:
	input_filename = args.input_file
else:
	raise Exception("Must specify an input file")

# Open the input file and read it to an array
try:
	with open (input_filename) as file:
		file_line_array = file.readlines()
except:
	raise Exception("File error")

result = wxbparse(file_line_array)

table = PrettyTable()
table.field_names = ["Airport", "City", "Cost", "Forecast", "URL"]

widgets = [Bar(), ' ', Percentage(), ' ', ETA()]
progress = progressbar.ProgressBar(widgets=widgets)

print("Retrieving")
for city in progress(result['cities']):
	station = station_info(city['airport'])
	point_string = format(station['geometry']['coordinates'][1], '.5f') + "," + format(station['geometry']['coordinates'][0], '.5f')
	point = point_info(point_string)
	table.add_row([city['airport'], city['city'], int(city['points']), format(city['forecast'], '.2f'), point['properties']['forecastHourly']])

table.sortby = "Cost"
table.reversesort = True

print(result['metadata']['battle_title'] + " - Entry Fee: $" + result['metadata']['entry_fee'])
print(result['metadata']['begins'] + " - " + result['metadata']['ends'])
print(table)