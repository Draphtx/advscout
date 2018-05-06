import gpxpy
import gpxpy.gpx
from haversine import Haversine

gps_rawdata = open('Piedmont-ADV-Routes.gpx', 'r')

gpx = gpxpy.parse(gps_rawdata)

# Manually specifying a search radius for a POC
radius = 1000  # feet

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

    avg_pds = avg_pd(points)
    pointer = 0
    active_point = points[pointer]

    while True:
        try:
            pointer += 1
            if not (Haversine([active_point.latitude, active_point.longitude], [points[pointer].latitude, points[pointer].longitude]).feet > (search_radius - avg_pds)):
                # print "Discarding point {0}".format(points[pointer].name)
                pass
            else:
                # print "Accepting point {0}".format(active_point.name)
                groomed_points.append(active_point)
                active_point = points[pointer - 1]
        except IndexError:
            # print "Accepting point {0}".format(points[pointer-1].name)
            groomed_points.append(points[pointer - 1])
            return groomed_points


def main():
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


if __name__ == '__main__':
    main()
    exit()

#    print route
#    print 'Route: {name}'.format(name=route.name)
#    for point in route.points:
#
#        print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation)
