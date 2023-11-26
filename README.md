# PlacesToMap
Show on map where you were


### How to use
1. Fill the database.csv file
	- Where (mandatory): name of the place: it will be geocoded in [osm.org](https://osm.org)
	- From (mandatory): start date in YYYY.MM.DD format
	- To (mandatory): end date in YYYY.MM.DD format
	- Who, (min 1 name mandatory): Participants, comma separated

2. Execute the processData.py script.
3. Check the ./geolocator/not_found.txt file. These places are not found in [osm.org](https://osm.org), fix it in the database.csv. 
4. Repeat 1-3 untill every place found