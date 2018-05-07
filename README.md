# advscout
Flesh out your adventure with configurable waypoint crawling!

## Summary
I'm putting together a little tool to help me in planning long-distance motorcycle adventure riding. The basic idea is
to allow the user to provide an existing GPS route as well as some parameters for what nearby location types they would
be interested in (e.g. restaurants, gas stations, Walmarts, etc). Leveraging the Google Maps API, the
script will crawl the route and search for these location types within a user-defined radius around the route's points. 
These new waypoints are labeled by category and business name and added to the GPX data for export to a GPX file. In 
this way adventurers can have access to important stops without manually mapping the whole route and without needing 
Google search capabilities on the trail.

## What problem is this solving?
For those unfamiliar with the term, Adventure motorcycling (popularly shortened to ADV) refers to long-distance riding, 
often in remote or isolated locations. The dedicated adventure rider may be alone for hours or even days at a time, and 
often necessarily find themselves without cellular reception or area wifi due to the terrain, atmospheric conditions, or 
simply the remoteness of their location.

For this reason, offline maps (including traditional maps, purpose-built GPS units, and pre-cached map information on 
cell phones or tablets) are an extremely important feature in most ADV riders' toolsets for basic way-finding and 
planning stops for fuel, food, and lodging.

Paper maps are often detailed and reliable but may be out of date and, even at their best, show only the points of 
interest that the map-maker deemed important enough to mark.

Many purpose-built GPS units (Garmin, TomTom) allow the user to search for nearby resources offline, but often have 
inconvenient UIs that make it difficult to assess the trip ahead at a glance; they are good at showing you what is 
close by, but not necessarily what is coming. They also may contain outdated or incorrect information that will not be 
filtered out until the manufacturer's next update. Finally, they are quite expensive and out of the budget of some riders.

Pre-cached maps on smart devices, meanwhile, are easy to update and are financially accessible to most riders. However 
these are normally not searchable without a data connection, and while users can mark potential stops ahead of time as 
waypoints it is a laborious manual process to analyze hundreds or thousands of miles of route data looking for fuel, 
motels, campgrounds, and restaurants, and marking each possibility.

ADVScout seeks to automate this process by analyzing the user's predefined GPX route and creating additional waypoints 
for various establishments and points-of-interest which the user has specified. The resulting file may be uploaded to 
Google's 'My Maps' for caching, various smartphone and tablet GPS apps, or purpose-built units like Garmin and TomTom. In this way 
a rider can get a full assessment of potential resources along the route and can use this information while offline to 
inform their stops.
 
## How it works
ADVScout is a simple application which seeks to provide the most relevant information with as little user input as 
possible. To this end the script will analyze the route(s) in the GPX file, simplify the route data to minimize API 
calls (the logic for this is not yet set-in-stone), and then look for establishments within a user-defined radius of the 
remaining waypoints.
### Example
A user has a GPX file with route data for the Transamerica Trail, a popular ADV motorcycling route. The user is 
interested in the location of any hospitals, gas stations, and hotels along his route. 
* He submits the file and chooses the three Google Maps categories 'gas_station,restaurant,hospital', and sets a radius 
of 2 miles for results.
* ADVScout looks at his route data and determines that 2/3 of his route's waypoints are within the search radius of the 
next waypoint, and so determines to only query from the remaining 1/3 as this will provide sufficient search coverage.
* Using the Google Maps API, each of these 'primary' waypoints is searched for hospitals, gas stations, and restaurants 
within a 2-mile radius. Any results are preserved and combined with the results from other waypoints.
* Once each primary waypoint has been analyzed, the combined results are categorized and additional GPS waypoints are 
created with the naming convention resembling 'advs:restaurant:Wendys' to allow for simple filtering in various 
applications.
* The new waypoints are added to the GPS data and exported to a .gpx file, which can then be loaded into other GPS 
software or hardware for later access.

## Shortcomings
ADVScout is only as reliable as the data and input provided to it. While Google Maps data is fairly reliable, be aware 
of the following:
* Google Maps is not always right! If you are relying on this information for critical, life-or-death purposes, I 
suggest calling ahead if possible to ensure that the establishment is open and ready for you.
* If your route is extremely simplified (i.e. has waypoints that are further apart than the search radius) some areas 
may not be searched.
* Some GPS software and hardware limits the total number of location waypoints (usually separate from track/route 
waypoints) that can be stored, so a very long route or one which passes through densely-populated areas with many search 
results may produce a file that exceeds your device's limitations. I'll think about ways to let the user filter results for this 
reason.
* It is possible to end up with results that are not easily reached from your route; e.g. a hospital may be within your 
search radius but be extremely difficult to reach from the route because of a river or mountain, and therefore useless. 
For this reason I suggest setting the radius to 5 miles or less.
* Google Maps calls do, in fact, cost money. An extremely long route with a tiny search radius for all categories could 
result in thousands or even tens of thousands of API calls. For this reason free ADVScout searches will be limited in 
various ways that have not been determined at the time of this writing, probably through a (minimally expensive) 
paid model for more complex searches.