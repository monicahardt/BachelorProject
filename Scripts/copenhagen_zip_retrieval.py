import geocoder
import json
import re
from geopy.geocoders import Nominatim
import csv
from geopy.location import Location

geolocator = Nominatim(user_agent="my_geocoder")

# go through the json file to locate all addresses with incorrect zipcode
# then try to retrieve the zipcode again
f = open('Data/data.json')
data = json.load(f)

#retrieve zipcode
def getZip(info):
    pattern = r'\d{4}'
    match = re.search(pattern, info)
    if match is not None:
        return match.group()
    else :
        return

addresses_incorrect_location = []
# we have some json objects where the address exists but the info is null. This happens in 1602 cases (assume this is where the geolocator failed)
for address, info in data.items():
    if info is not None: 
        zip_code = getZip(info['address'])  # Extract zip code from address could be empty
        if zip_code is not None:
            if not 1000 <= int(zip_code) <= 4999: #for now removing all failed zipcodes in Jylland
                 addresses_incorrect_location.append(address)

print(f"The amount of addresses to look up is: {len(addresses_incorrect_location)}")

added_location_to_coordinate = {}

for place in addresses_incorrect_location:
    locations = geocoder.osm(place, maxRows=10)
    for location_found in locations:
        zip = location_found.postal
        #print(f"zip found for location: {location_found} was: {zip}")
        if zip is not None:
            try:
                if 1000 <= int(zip) <= 4999:
                    added_location_to_coordinate[place] = location_found
                    print(location_found)  
            except:
                print(f"Failed to convert zip for location {place}, found zip {zip}") 
                
# #save as csv file
# with open('Data/added_location_coord.csv', 'w') as f: 
#     w = csv.DictWriter(f, added_location_to_coordinate.keys())
#     w.writeheader()
#     w.writerow(added_location_to_coordinate)

def location_encoder(obj):
    return {
            "latitude"  : obj.lat, 
            "longitude" : obj.lng,
            "address"   : obj.address,
            }


#Store the dict as JSON
with open("added_data.json", "w") as file:
    json.dump(added_location_to_coordinate, file, default=location_encoder, indent=4)

