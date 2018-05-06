#!/usr/bin/python

import requests
import optparse

parser = optparse.OptionParser()
parser.add_option('-k', '--key',
                  dest='key',
                  default=None,
                  help="Supply GMaps API key")

(options, args) = parser.parse_args()
api_key = options.key

class GMaps_Place_Nearby():
    def __init__(self, coordinates, category, radius=1500, keyword=None):
        self.base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        self.results = {}
        self.location = coordinates
        self.radius = int(radius)
        self.category = category

    def query(self):
        gmaps_url = '{base_url}location={location}&radius={radius}&type={category}&key={key}'.format(
            base_url=self.base_url, location=self.location, radius=self.radius, category=self.category, key=api_key
        )
        self.results = requests.get(gmaps_url).json()
        return self.results



def main():
    current_coordinates = '33.7516104,-84.3594624'  # Krog Street Market
    r = GMaps_Place_Nearby(current_coordinates, 'restaurant')
    results = r.query()
    print results



if __name__ == '__main__':
    main()
    exit()
