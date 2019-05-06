# Functions for pulling data from the NWS API
from urllib.request import urlopen
import json

def station_info(station):
	base_url = "https://api.weather.gov/stations/"
	request_url = base_url + station
	response = urlopen(request_url)
	data = response.read().decode("utf-8")
	return json.loads(data)

def point_info(point_str):
	base_url = "https://api.weather.gov/points/"
	request_url = base_url + point_str
	response = urlopen(request_url)
	data = response.read().decode("utf-8")
	return json.loads(data)

def hourly_forecast(forecastHourly_url):
	response = urlopen(forecastHourly_url)
	data = response.read().decode("utf-8")
	return json.loads(data)
