"""Module that works with data about films, given in file locations.list, \
creates webmap with closest films to you.
    """
import argparse
import folium
import pandas
import geopy
import csv
from math import sin, cos, asin, sqrt, pi
import cords_locator


def create_parser() -> object:
    """returns parser object

    Returns:
        object: parser object
    """
    parser = argparse.ArgumentParser(description='year and location parser')
    parser.add_argument('year', type=int,
                        help='year, when films were shot')
    parser.add_argument('latitude', type=float,
                        help='latitude of location near which to search for films')
    parser.add_argument('longtitude', type=float,
                        help='longtitude of location near which to search for films')
    parser.add_argument('dst', type=str,
                        help='destination of dataset with films')

    return parser


def locations_year_filter(source: str, year: int) -> None:
    with open(source, 'rb') as file:
        lines = file.readlines()[14:]

    searched_films = []

    for index, line in enumerate(lines):
        new_line = str(line, 'ISO-8859-1').split('\t')
        if new_line[0].find(f'({year})') != -1:
            new_line[-1] = new_line[-1].rstrip('\n')
            year_space = new_line[0].rfind(' ')
            new_line.insert(1, new_line[0][year_space + 2:-1])
            new_line[0] = new_line[0][:year_space]
            searched_films.append(new_line)

    return searched_films


def find_distance_on_sphere(my_lat: float, my_lng: float, lat: float, lng: float) -> float:
    RADIUS = 6367000
    lat1 = my_lat * pi / 180
    lng1 = my_lng * pi / 180
    lat2 = lat * pi / 180
    lng2 = lng * pi / 180

    dist = 2 * RADIUS * asin(sqrt(sin((lat1 - lat2) / 2) **
                                  2 + cos(lat1) * cos(lat2) * sin((lng1 - lng2) / 2) ** 2))
    return dist


def find_closest_films(dataset: str, year: str, cord: tuple) -> list:
    all_data = pandas.read_csv(
        dataset, sep='","', quoting=csv.QUOTE_NONE)
    data = all_data.loc[all_data['Year'] == year]
    films = data['Name']
    cords = data['Coordinates']
    indexs = data.index

    my_lat = cord[0]
    my_lng = cord[1]
    closest_locations = [(100000000, 1) for i in range(5)]
    for index, cord in zip(indexs, cords):
        if cord == 'None"' or cord == 'location is undefined"':
            continue
        else:
            lat = float(cord[1:cord.find(',')])
            lng = float(cord[1 + cord.find(','): -2])
            dist = find_distance_on_sphere(my_lat, my_lng, lat, lng)

            closest_locations.append((dist, index))
            closest_locations.sort(key=lambda x: x[0])
            closest_locations.pop(-1)

    closest_films = [
        (closest_locations[i][0], films[closest_locations[i][1]], cords[closest_locations[i][1]]) for i in range(5)]

    return closest_films


def map_creator(lat, lng, year, films) -> None:
    html = '''<h4>Film info:</h4>
Name: {},<br>
<a href=https://www.imdb.com/find?q={}>IMDb page</a>
'''
    map = folium.Map(location=[lat, lng], zoom_start=8)

    map.add_child(folium.Marker(location=[lat, lng],
                                popup="я тут!",
                                icon=folium.Icon()))

    group = folium.FeatureGroup(name=f'{year} films')

    for film in films:
        cord = film[2]
        lat = float(cord[1:cord.find(',')])
        lng = float(cord[1 + cord.find(','): -2])
        iframe = folium.IFrame(html=html.format(film[1][1:], '+'.join(film[1][1:].split())),
                               width=300,
                               height=100)
        group.add_child(folium.Marker(location=[lat, lng],
                                      popup=folium.Popup(iframe),
                                      icon=folium.Icon(color="green")))

    map.add_child(group)
    map.add_child(folium.LayerControl())

    map.save('Map_1.html')


def main_func(year: int, latitude: float, longtitude: float, dst: str) -> None:
    cords_locator.main(dst, year)
    films = find_closest_films(
        'dump_films.csv', str(year), (latitude, longtitude))
    map_creator(latitude, longtitude, year, films)


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()

    main_func(args.year, args.latitude, args.longtitude, args.dst)
