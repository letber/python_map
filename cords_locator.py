from opencage.geocoder import OpenCageGeocode
from main import locations_year_filter
import functools
from geopy.geocoders import Nominatim

KEY = 'b338f89a275046cc8e8ecf2568787f67'


@functools.lru_cache(maxsize=250000)
def locator(location: str) -> tuple:
    geocoder = OpenCageGeocode(KEY)
    results = geocoder.geocode(location)
    try:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        coordinates = (lat, lng)
    except IndexError:
        coordinates = (None)
    return coordinates


@functools.lru_cache(maxsize=250000)
def locator_n(location: str) -> tuple:
    geolocator = Nominatim(user_agent="my-request", timeout=3)
    loc = geolocator.geocode(location)
    try:
        coordinates = (loc.latitude, loc.longitude)
    except AttributeError:
        coordinates = None
    return coordinates


def main(source: str, year: int) -> list:
    films_list = locations_year_filter(source, year)
    films_cords = []
    for film in films_list:
        query = film[-1]
        year = film[1]
        cords = locator_n(query)
        films_cords.append(f'"{film[0]}","{year}","{query}","{cords}"\n')
    
    with open('dump_films.csv', mode='w') as file:
        # Uncomment if you don't have dump_films.csv file, also change open mode to w
        file.write('Name","Year","Location","Coordinates\n')
        file.writelines(films_cords)
    
    return films_cords


if __name__ == '__main__':
    year = int(input('Please enter the year: '))
    main('locations_24.list', year)

