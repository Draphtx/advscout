import gpxpy
import gpxpy.gpx
from haversine import Haversine

gps_rawdata = open('Piedmont-ADV-Routes.gpx', 'r')

gpx = gpxpy.parse(gps_rawdata)

print gpx


def avg_pd(points):
    pds = []
    for index, item in enumerate(points[:-1]):
        next_point = points[index + 1]
        pd = Haversine([item.longitude, item.latitude], [next_point.longitude, next_point.latitude])
        pds.append(pd.feet)
    return sum(pds)/len(pds)


def groom_points(points, pd_avg):
    return [item for index, item in enumerate(points[:-1]) if Haversine([item.latitude, item.longitude], [points[index+1].latitude, points[index+1].longitude]).feet < pd_avg]



def main():
    for route in gpx.routes:
        print "Analyzing Route: {name}".format(name=route.name)

        pd_avg = avg_pd(route.points)
        print "Average distance between points: {pd} feet".format(pd=pd_avg)

        groomed_points = groom_points(route.points, pd_avg)

        print "Groomed points to {0} from {1}".format(len(groomed_points), len(route.points))

if __name__ == '__main__':
    main()
    exit()

#    print route
#    print 'Route: {name}'.format(name=route.name)
#    for point in route.points:
#
#        print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation)
