import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderUnavailable
from geopy.exc import GeocoderQueryError
import time

geolocator = Nominatim(user_agent="my_geocoder")
    
def create_unique_list(sequences):
    unique_stations_set = set()
    for seq in sequences:
        for place in seq:
            unique_stations_set.add(place)
    # Convert the set back to a list
    unique_stations_list = list(unique_stations_set)
    return unique_stations_list


location_to_coordinate = {}
def add_coordinate_to_station(station):    
    retries = 3
    while retries > 0:
        try: 
            if station.__contains__("Metro"):
                station_metro = str.replace(station, "(Metro)", "").strip()
                coord = geolocator.geocode(station_metro)
            else:    
                coord = geolocator.geocode(station)    
                
            location_to_coordinate[station] = coord
            break  # Exit the retry loop if successful
        except GeocoderTimedOut as e:
            retries -= 1
            if retries == 0:
                print(f" Max retries exceeded for {station}. Skipping...")
            time.sleep(1)  # Add a delay between retries to avoid overwhelming the server
        except GeocoderUnavailable as e:
            print(f"Geocoder unavailable: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying
        except GeocoderQueryError as e:
            print(f"Geocoder query error: {e}")
            break  # Exit the retr  y loop if there's a query error


def fill_loc_to_coord(unique_stations_list):
    for station in unique_stations_list:
        add_coordinate_to_station(station)
    
    
def get_sequences(path):
    return pd.read_csv(path).to_list()

def save_dict_as_csv(dict):
    import csv
    my_dict = {"test": 1, "testing": 2}
    with open('Data/location_coord.csv', 'w') as f: 
        w = csv.DictWriter(f, my_dict.keys())
        w.writeheader()
        w.writerow(my_dict)
    
def main():
    path = 'Data/sequence_list.csv'
    seq = get_sequences(path)
    unique_list = create_unique_list(seq)
    fill_loc_to_coord(unique_list)
    
main()