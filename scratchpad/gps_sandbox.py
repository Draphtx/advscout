
import requests
import optparse
import gpxpy
import gpxpy.gpx
from haversine import Haversine


valid_categories = [
    'accounting', 'airport', 'amusement_park', 'aquarium', 'art_gallery', 'atm', 'bakery', 'bank', 'bar',
    'beauty_salon', 'bicycle_store', 'book_store', 'bowling_alley', 'bus_station', 'cafe', 'campground', 'car_dealer',
    'car_rental', 'car_repair', 'car_wash', 'casino', 'cemetery', 'church', 'city_hall', 'clothing_store',
    'convenience_store', 'courthouse', 'dentist', 'department_store', 'doctor', 'electrician', 'electronics_store',
    'embassy', 'fire_station', 'florist', 'funeral_home', 'furniture_store', 'gas_station', 'gym', 'hair_care',
    'hardware_store', 'hindu_temple', 'home_goods_store', 'hospital', 'insurance_agency', 'jewelry_store', 'laundry',
    'lawyer', 'library', 'liquor_store', 'local_government_office', 'locksmith', 'lodging', 'meal_delivery',
    'meal_takeaway', 'mosque', 'movie_rental', 'movie_theater', 'moving_company', 'museum', 'night_club', 'painter',
    'park', 'parking', 'pet_store', 'pharmacy', 'physiotherapist', 'plumber', 'police', 'post_office',
    'real_estate_agency', 'restaurant', 'roofing_contractor', 'rv_park', 'school', 'shoe_store', 'shopping_mall',
    'spa', 'stadium', 'storage', 'store', 'subway_station', 'supermarket', 'synagogue', 'taxi_stand', 'train_station',
    'transit_station', 'travel_agency', 'veterinary_care', 'zoo']

parser = optparse.OptionParser()
parser.add_option('-K', '--key',
                  dest='key',
                  default=None,
                  help="Supply GMaps API key")
parser.add_option('-k', '--keywords',
                  dest='keywords',
                  default=None,
                  help='Supply keywords to refine search. This will necessarily exclude results from certain '
                       'categories, so be cautious that you do not over-refine your search.')
parser.add_option('-f', '--input-file',
                  dest='infile',
                  default=None,
                  help='Specify the GPX file that you would like to import.')
parser.add_option('-o', '--output-file',
                  dest='outfile',
                  default=None,
                  help='Specify the output GPX file. If left empty, output will replace the original file passed as '
                       'input.')
parser.add_option('-c', '--categories',
                  dest='categories',
                  default='gas_station',
                  help='A comma-separated list of Google Maps location categories in which to search. This can include '
                       'any of the following: | {cats}'.format(cats=' | '.join(valid_categories)))
(options, args) = parser.parse_args()
api_key = options.key

print options.categories
gps_rawdata = open(options.infile, 'r')
gpx = gpxpy.parse(gps_rawdata)

# Manually specifying a search radius for a POC
radius = 1609  # meters

print gpx


def avg_pd(points):
    pds = []
    for index, item in enumerate(points[:-1]):
        next_point = points[index + 1]
        pd = Haversine([item.longitude, item.latitude], [next_point.longitude, next_point.latitude])
        pds.append(pd.feet)
    return sum(pds)/len(pds)


def groom_points(points, search_radius):
    groomed_points = []

    pointer = 0
    active_point = points[pointer]

    while True:
        try:
            pointer += 1
            if not (Haversine([active_point.latitude, active_point.longitude], [points[pointer].latitude, points[pointer].longitude]).meters * 2 > (search_radius)):
                # print "Discarding point {0}".format(points[pointer].name)
                pass
            else:
                # print "Accepting point {0}".format(active_point.name)
                groomed_points.append(active_point)
                active_point = points[pointer - 1]
        except IndexError:
            print "Accepting point {0}".format(points[pointer-1].name)
            groomed_points.append(points[pointer - 1])
            return groomed_points


def search_gmaps(points):
    results = {}
    maps_calls = 0
    for point in points:
        for category in (options.categories.split(',')):
            print "Searching {lat},{long} for places with category {cat}".format(
                lat=point.latitude, long=point.longitude, cat=category
            )
            base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
            gmaps_url = gmaps_url = '{base_url}location={location}&radius={radius}&type={category}&key={key}'.format(
                base_url=base_url, location='{lat},{long}'.format(lat=point.latitude, long=point.longitude),
                radius=radius, category=category, key=api_key
            )
            maps_calls += 1

            gresults = requests.get(gmaps_url).json()
            for item in gresults['results']:
                results[item['name']] = item
    print "Made {calls} GMaps calls and returned {results} results".format(calls=maps_calls, results=len(results))
    return results


def main():
    overall_results = {}
    for index, route in enumerate(gpx.routes):
        print "Analyzing Route: {name}".format(name=route.name)

        pd_avg = avg_pd(route.points)
        print "Average distance between points: {pd} feet".format(pd=pd_avg)

        groomed_points = groom_points(route.points, radius)

        print "Groomed points to {0} from {1}".format(len(groomed_points), len(route.points))

        pd_avg = avg_pd(groomed_points)
        print "Average distance between points: {pd} feet".format(pd=pd_avg)

        gpx.routes[index].points = groomed_points
        print len(gpx.routes[index].points)
        print()

    for index, route in enumerate(gpx.routes):
        results = search_gmaps(route.points)
        print results
        overall_results.update(results)

    print "{0} results total".format(len(overall_results))
    print overall_results

    print len(gpx.waypoints)

    for waypoint, details in overall_results.iteritems():
        print waypoint, details
        w = gpxpy.gpx.GPXWaypoint(details['geometry']['location']['lat'],
                                  details['geometry']['location']['lng'],
                                  name=waypoint)
        gpx.waypoints.append(w)
    print len(gpx.waypoints)

    with open(options.outfile, 'w') as record:
        record.write(gpx.to_xml())


if __name__ == '__main__':
    main()
    exit()

#    print route
#    print 'Route: {name}'.format(name=route.name)
#    for point in route.points:
#
#        print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation)
