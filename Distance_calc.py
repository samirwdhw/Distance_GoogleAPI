import json, urllib
import requests
import geopy.distance

API_KEY = 'AIzaSyC8m1yNa6eDGE5VLR1GjQ-5Mz_WyoM-5Kc'


#To be able to pass all locations in one call
def addLocations(content):

	validArgument = ''

	for locations in content:
		validArgument += locations + '|'

	return validArgument

#To return the latitude and longitude of a location
def getLatLong(location):


	payload = {'address': location}
	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params = payload)

	parsed_json = response.json()

	if parsed_json['status'] == "OK":
		latitude = parsed_json['results'][0]['geometry']['location']['lat']
		longitude = parsed_json['results'][0]['geometry']['location']['lng']

		return latitude, longitude
	
	else:
		return "no", "no"

#To calculae great circle distance
def getBirdDist(lat_long):
	global IITB_latLong

	return (geopy.distance.vincenty(IITB_latLong, lat_long).meters)/1000



#Array of lists to store locations with their distances
locationDistances = []

#Araay of locations with not found 
locationNotFound = []

user_origin = "IIT Bombay"

content = [line.rstrip('\n') for line in open('places.txt')]

payload  = {'origins': user_origin, 'destinations': addLocations(content), 'key': API_KEY}

response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?', params = payload)


parsed_json  = response.json()

#A variable to increment with the loop
i = 0

for row in parsed_json['rows'][0]['elements']:
	#If a valid path is found
	if row['status'] == "OK":
		locationDistances.append(
									{
										'location': content[i], 
										'value': row['distance']['value'],
										'distance': row['distance']['text']
									}
								)

	#If not
	else:
		locationNotFound.append(content[i])

	i += 1


#To sort the list
locationDistances.sort()
sortedList = sorted(locationDistances, key= lambda locationDistances: locationDistances['value'])

for i in sortedList:
	print i['location'] + ": " + i['distance']

for notFound in locationNotFound:
	print notFound + ": No path found" 

#################################################################################################################################
#To calculate the bird's line distance

print " "
print " "
print " "

#To empty the lists 
del locationDistances[:]
del locationNotFound[:]

lat_long = []

IITB_latLong = getLatLong("IIT Bombay")

i = 0
for place in content:
	
	latitude, longitude =  getLatLong(place)


	#if valid latitude is there
	if latitude != "no":
		locationDistances.append(
									{
										'value': getBirdDist((latitude, longitude)),
										'location': content[i]
									}
								)
	else: 
		locationNotFound.append(content[i])
	i += 1

locationDistances.sort()
sortedList = sorted(locationDistances, key= lambda locationDistances: locationDistances['value'])

for i in sortedList:
	print i['location'] + ": " + str(i['value'])
for notFound in locationNotFound:
	print notFound + ": No path found" 