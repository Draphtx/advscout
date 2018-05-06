
import requests
import optparse
import gpxpy
import gpxpy.gpx
from haversine import Haversine

parser = optparse.OptionParser()
parser.add_option('-k', '--key',
                  dest='key',
                  default=None,
                  help="Supply GMaps API key")

(options, args) = parser.parse_args()
api_key = options.key

gps_rawdata = open('tat1_routes2.gpx', 'r')
category = 'gas_station'
gpx = gpxpy.parse(gps_rawdata)

# Manually specifying a search radius for a POC
radius = 5280  # feet

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
            if not (Haversine([active_point.latitude, active_point.longitude], [points[pointer].latitude, points[pointer].longitude]).feet * 2 > (search_radius)):
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
        print point.latitude, point.longitude
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        gmaps_url = gmaps_url = '{base_url}location={location}&radius={radius}&type={category}&key={key}'.format(
            base_url=base_url, location='{lat},{long}'.format(lat=point.latitude, long=point.longitude), radius=5280, category=category, key=api_key
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
        w = gpxpy.gpx.GPXWaypoint(details['geometry']['location']['lat'], details['geometry']['location']['lng'], name=waypoint)
        gpx.waypoints.append(w)
    print len(gpx.waypoints)

    with open('gpx_to_xml_output.gpx', 'w') as record:
        record.write(gpx.to_xml())





if __name__ == '__main__':
    main()
    exit()

#    print route
#    print 'Route: {name}'.format(name=route.name)
#    for point in route.points:
#
#        print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation)
