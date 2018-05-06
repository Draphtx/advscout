# advscout
Flesh out your adventure with configurable waypoint crawling!

## Summary
I'm putting together a little tool to help me in planning long-distance motorcycle adventure riding. The basic idea is
to allow the user to provide an existing GPS route as well as some parameters for what nearby location types they would
be interested in (e.g. restaurants, gas stations, Walmarts, etc). Leveraging their own Google Maps API account, the
script will crawl the route and query Google maps every from every x amount of points for those location types. The
script will then add those waypoints to the existing GPS data and spit out a new file with the route information and
the additional waypoints. In this way adventurers can have access to important stops without manually mapping the whole
route and without needing Google search capabilities on the trail.