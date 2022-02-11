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


if __name__ == '__main__':
    c = [40.7306, -73.9352]
    year = input()
    # l = locations_year_filter('locations_6.list', year)
    # print(l, len(l))

    # pars = create_parser()
    # args = pars.parse_args()

    # print(args.latitude, args.longtitude, args.dst)
