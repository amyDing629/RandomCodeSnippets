"""CSC108: Fall 2020 -- Assignment 2: Rent-a-bike

This code is provided solely for the personal and private use of
students taking the CSC108 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, and Anya Tafliovich.
"""

import math
from typing import List, TextIO

"""For simplicity, we'll use "Station" in our type contracts to indicate that
we mean a list containing station data. 

You can read "Station" in a type contract as:
List[int, str, float, float, int, int, int, bool, bool]

where the values at each index represent the station data as described in the 
handout on Quercus.
"""

# A set of constants, each representing a list index for station information.
ID = 0
NAME = 1
LATITUDE = 2
LONGITUDE = 3
CAPACITY = 4
BIKES_AVAILABLE = 5
DOCKS_AVAILABLE = 6
NO_KIOSK = 'SMART'

# For use in a helper function
EARTH_RADIUS = 6371

### SAMPLE DATA TO USE IN DOCSTRING EXAMPLES ####

SAMPLE_STATIONS = [
    [7090, 'Danforth Ave / Lamb Ave',
     43.681991, -79.329455, 15, 4, 10],
    [7486, 'Gerrard St E / Ted Reeve Dr',
     43.684261, -79.299332, 24, 5, 19],
    [7571, 'Highfield Rd / Gerrard St E - SMART',
     43.671685, -79.325176, 19, 14, 5]]

HANDOUT_STATIONS = [
    [7000, 'Ft. York / Capreol Crt.',
     43.639832, -79.395954, 31, 20, 11],
    [7001, 'Lower Jarvis St SMART / The Esplanade',
     43.647992, -79.370907, 15, 5, 10]]


#########################################


####### BEGIN HELPER FUNCTIONS ####################

def is_number(value: str) -> bool:
    """Return True if and only if value represents a decimal number.

    >>> is_number('csc108')
    False
    >>> is_number('  108 ')
    True
    >>> is_number('+3.14159')
    True
    """

    return value.strip().lstrip('-+').replace('.', '', 1).isnumeric()


def get_lat_lon_distance(lat1: float, lon1: float,
                         lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by   
    (lat1, lon1) and (lat2, lon2), rounded to the nearest metre.
    
    >>> get_lat_lon_distance(43.659777, -79.397383, 43.657129, -79.399439)
    0.338
    >>> get_lat_lon_distance(43.67, -79.37, 55.15, -118.8)
    3072.872
    """

    # This function uses the haversine function to find the distance between 
    # two locations. You do NOT need to understand why it works.
    # You will just need to call on the function and work with what it returns.
    # Based on code at goo.gl/JrPG4j

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1),
                              math.radians(lon2), math.radians(lat2))

    # haversine formula t
    lon_diff = lon2 - lon1
    lat_diff = lat2 - lat1
    a = (math.sin(lat_diff / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return round(c * EARTH_RADIUS, 3)


# It isn't necessary to call this function to implement your bikes.py
# functions, but you can use it to create larger lists for testing.
# See the main block below for an example of how to do that.
def csv_to_list(csv_file: TextIO) -> List[List[str]]:
    """Read and return the contents of the open CSV file csv_file as a list of
    lists, where each inner list contains the values from one line of csv_file.

    Docstring examples not given since results depend on data to be input.
    """

    # Read and discard header.
    csv_file.readline()

    data = []
    for line in csv_file:
        data.append(line.strip().split(','))
    return data


####### END HELPER FUNCTIONS ####################

def clean_data(data: List[list]) -> None:
    """Convert each string in data to an int if and only if it represents a
    whole number, and a float if and only if it represents a number that is not 
    a whole number.

    >>> d = [['abc', '123', '45.6', 'car', 'Bike']]
    >>> clean_data(d)
    >>> d
    [['abc', 123, 45.6, 'car', 'Bike']]
    >>> d = [['ab2'], ['-123'], ['BIKES', '3.2'], ['3.0', '+4', '-5.0']]
    >>> clean_data(d)
    >>> d
    [['ab2'], [-123], ['BIKES', 3.2], [3, 4, -5]]
    """

    for sublist in data:
        for i in range(len(sublist)):
            val = sublist[i]
            if is_number(val) is True:
                if val[0] == '+':
                    val = float(val[1:])
                elif val[0] == '-':
                    val = 0 - float(val[1:])
                else:
                    val = float(val)
                if int(val) == val:
                    val = int(val)
                sublist[i] = val


def has_kiosk(station: "Station") -> bool:
    """Return True if and only if the given station has a kiosk.    
    
    >>> has_kiosk(SAMPLE_STATIONS[0])
    True
    >>> has_kiosk(SAMPLE_STATIONS[2])
    False
    """
    return NO_KIOSK not in station[1]


def get_station_info(station_id: int, stations: List["Station"]) -> list:
    """Return a list containing the following information from stations
    about the station with id number station_id:
        - station name (str)
        - number of bikes available (int)
        - number of docks available (int)
        - whether or not the station has a kiosk (bool)
    (in this order)

    If station_id is not in stations, return an empty list.

    >>> get_station_info(7090, SAMPLE_STATIONS)
    ['Danforth Ave / Lamb Ave', 4, 10, True]
    >>> get_station_info(7571, SAMPLE_STATIONS) 
    ['Highfield Rd / Gerrard St E - SMART', 14, 5, False]
    """
    for sublist in stations:
        if sublist[0] == station_id:
            return [sublist[1], sublist[-2], sublist[-1], has_kiosk(sublist)]


def get_total(index: int, stations: List["Station"]) -> int:
    """Return the sum of the column in stations given by index.

    Precondition: the items in stations at the position
                  that index refers to are ints.

    >>> get_total(BIKES_AVAILABLE, SAMPLE_STATIONS)
    23
    >>> get_total(DOCKS_AVAILABLE, SAMPLE_STATIONS)
    34
    """
    rst = 0
    for sublist in stations:
        rst += sublist[index]
    return rst


def get_stations_with_n_docks(n: int, stations: List["Station"]) -> List[int]:
    """Return a list containing the station IDs for the stations in stations
    that have at least n docks available, in the same order as they appear
    in stations.

    Precondition: n >= 0

    >>> get_stations_with_n_docks(2, SAMPLE_STATIONS)
    [7090, 7486, 7571]
    >>> get_stations_with_n_docks(12, SAMPLE_STATIONS)
    [7486]
    """
    rst = []
    for sublist in stations:
        if sublist[-1] >= n:
            rst.append(sublist[0])
    return rst


def get_nearest_station(lat: float, lon: float, with_kiosk: bool,
                        stations: List['Station']) -> int:
    """Return the id of the station from stations that is nearest to the
    station with id station_id (and is different from station_id). If
    with_kiosk is True, return the id of the closest station with a
    kiosk.

    In the case of a tie, return the ID of the first station in
    stations with that distance.

    Preconditions: len(stations) > 1

    If with_kiosk, then there is at least one station in stations with a kiosk 
    that has an id different from station_id.

    >>> get_nearest_station(43.671134, -79.325164, False, SAMPLE_STATIONS)
    7571
    >>> get_nearest_station(43.674312, -79.299221, True, SAMPLE_STATIONS)
    7486
    """
    mini = [None, 1000000000000]
    for sublist in stations:
        if with_kiosk is not True or has_kiosk(sublist) is True:
            distance = ((sublist[2] - lat) ** 2 + (sublist[3] - lon) ** 2) ** 0.5
            if 0 < distance < mini[1]:
                mini = [sublist[0], distance]
    return mini[0]


def rent_bike(station_id: int, stations: List["Station"]) -> bool:
    """Update the available bike count and the docks available count
    for the station in stations with id station_id as if a single bike was
    removed, leaving an additional dock available. Return True if and only
    if the rental was successful.

    Precondition: station_id will appear in stations.

    >>> station_id = SAMPLE_STATIONS[0][ID]
    >>> original_bikes_available = SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    >>> original_docks_available = SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    >>> rent_bike(station_id, SAMPLE_STATIONS)
    True
    >>> original_bikes_available - 1 == SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    True
    >>> original_docks_available + 1 == SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    True
    >>> no_bike_station = [7090, 'Danforth Ave / Lamb Ave', \
    43.681991, -79.329455, 15, 0, 15]
    >>> station_id = no_bike_station[ID]
    >>> original_bikes_available = no_bike_station[BIKES_AVAILABLE]
    >>> original_docks_available = no_bike_station[DOCKS_AVAILABLE]
    >>> rent_bike(station_id, [no_bike_station])
    False
    >>> original_bikes_available == no_bike_station[BIKES_AVAILABLE]
    True
    >>> original_docks_available == no_bike_station[DOCKS_AVAILABLE]
    True
    """
    for sublist in stations:
        if sublist[0] == station_id:
            if sublist[-2] == 0:
                return False
            else:
                sublist[-2] = sublist[-2] - 1
                sublist[-1] = sublist[-1] + 1
                return True


def return_bike(station_id: int, stations: List["Station"]) -> bool:
    """Update the available bike count and the docks available count
    for station in stations with id station_id as if a single bike was added,
    making an additional dock unavailable. Return True if and only if the
    return was successful.

    Precondition: station_id will appear in stations.

    >>> station_id = SAMPLE_STATIONS[0][ID]
    >>> original_bikes_available = SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    >>> original_docks_available = SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    >>> return_bike(station_id, SAMPLE_STATIONS)
    True
    >>> original_bikes_available + 1 == SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    True
    >>> original_docks_available - 1 == SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    True
    >>> no_dock_station = [7090, 'Danforth Ave / Lamb Ave', \
    43.681991, -79.329455, 15, 15, 0]
    >>> station_id = no_dock_station[ID]
    >>> original_bikes_available = no_dock_station[BIKES_AVAILABLE]
    >>> original_docks_available = no_dock_station[DOCKS_AVAILABLE]
    >>> return_bike(station_id, [no_dock_station])
    False
    >>> original_bikes_available == no_dock_station[BIKES_AVAILABLE]
    True
    >>> original_docks_available == no_dock_station[DOCKS_AVAILABLE]
    True
    """
    for sublist in stations:
        if sublist[0] == station_id:
            if sublist[-1] == 0:
                return False
            else:
                sublist[-1] = sublist[-1] - 1
                sublist[-2] = sublist[-2] + 1
                return True


def redistribute_bikes(stations: List["Station"]) -> int:
    """Calculate the percentage of bikes available across all stations
    and evenly distribute the bikes so that each station has as close to the
    overall percentage of bikes available as possible. Remove bikes from a
    station if and only if the station is renting and there is a bike
    available to rent, and return a bike if and only if the station is
    allowing returns and there is a dock available. Return the difference
    between the number of bikes rented and the number of bikes returned.

    >>> handout_copy = [HANDOUT_STATIONS[0][:], HANDOUT_STATIONS[1][:]]
    >>> redistribute_bikes(handout_copy)
    0
    >>> handout_copy == [\
     [7000, 'Ft. York / Capreol Crt.', 43.639832, -79.395954, 31, 17, 14], \
     [7001, 'Lower Jarvis St SMART / The Esplanade', \
     43.647992, -79.370907, 15, 8, 7]]
    True
    >>> sample_copy = [SAMPLE_STATIONS[0][:], SAMPLE_STATIONS[1][:], \
                       SAMPLE_STATIONS[2][:]]
    >>> redistribute_bikes(sample_copy)
    -1
    >>> sample_copy == [\
    [7090, 'Danforth Ave / Lamb Ave', 43.681991, -79.329455, 15, 6, 8], \
    [7486, 'Gerrard St E / Ted Reeve Dr', 43.684261, -79.299332, 24, 10, 14], \
    [7571, 'Highfield Rd / Gerrard St E - SMART', 43.671685, -79.325176, \
    19, 8, 11]]
    True
    """
    tol_capacity = 0
    tol_bikes = 0
    for sublist in stations:
        tol_capacity += sublist[-3]
        tol_bikes += sublist[-2]
    percentage = tol_bikes / tol_capacity
    tol_diff = 0
    for sublist in stations:
        tar = percentage * sublist[-3]
        diff = round(sublist[-2] - tar)
        if diff < 0:
            for i in range(0 - diff):
                return_bike(sublist[0], stations)
        elif diff > 0:
            for i in range(diff):
                rent_bike(sublist[0], stations)
        tol_diff += diff
    return tol_diff


if __name__ == '__main__':
    pass

    # To test your code with larger lists, you can uncomment the code below to
    # read data from the provided CSV file.
    stations_file = open('stations.csv')
    bike_stations = csv_to_list(stations_file)
    stations_file.close()
    clean_data(bike_stations)
    print(bike_stations[:2])

    # For example,
    print('Testing get_stations_with_n_docks:',
          get_stations_with_n_docks(32, bike_stations) == [7030, 7242, 7285])
