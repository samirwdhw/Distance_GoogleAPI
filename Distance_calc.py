import json, urllib
import requests

#To be able to pass all locations in one call
def addLocations(content):

	validArgument = ''

	for locations in content:
		validArgument += locations + '|'

	return validArgument


API_KEY = 'AIzaSyC8m1yNa6eDGE5VLR1GjQ-5Mz_WyoM-5Kc'

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