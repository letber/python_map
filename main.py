"""Module that works with data about films, given in file locations.list,\

    """
import argparse
import folium
import pandas
import geopy


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


def map_creator(lat, lng, year) -> None:
    html = '''<h4>Churches information:</h4>
Name: {},<br>
IMDb page: {}
'''

    map = folium.Map(location = [lat, lng], zoom_start=10)

    group = folium.FeatureGroup(name=f'{year} films')

    group.add_child(folium.Marker(location=[40.7306, -73.9352],
                                popup="я тут!",
                                icon=folium.Icon()))
    
    map.add_child(group)
    map.add_child(folium.LayerControl())

    map.save('Map_1.html')


if __name__ == '__main__':
    c = [40.7306, -73.9352]
    year = input()
    l = locations_year_filter('locations_6.list', year)
    print(l, len(l))

    # pars = create_parser()
    # args = pars.parse_args()

    # print(args.latitude, args.longtitude, args.dst)
