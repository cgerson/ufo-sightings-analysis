# ufo-sightings-analysis

This repo holds my code and methods for an analysis of UFO sightings reports in the US. Raw data can be found at NUFORC's online <a href = "http://www.nuforc.org/webreports.html" target="_blank">UFO sightings database</a>.

The purpose of this analysis was to find the most "credible" sightings according to a number of factors (currently by number of similar reports). Analysis is ongoing.


###Code to collect:

I used the "wget" command to scrape 99,477 UFO sightings descriptions (summaries) from the NUFORC site. Essentially followed <a href = "http://blog.scotterussell.com/post/93524577748/ufo-data-science-how-we-get-data-part-2" target="_blank">this tutorial</a>.

Once all summaries were downloaded on my remote server, I used <b>BeautifulSoup</b> to scrape the relevant information and insert one by one in my <b>MongoDB</b> database. See "build_summaries.py" for the script.

The rest of the metadata of each UFO sighting (timestamp, location, duration and shape) were scraped and stored in a pandas dataframe, with the link to the sighting as it's unique ID. See "ufo_nosummary.pkl" for the data.


###Code to clean:

The summaries were filtered and stripped of punctuation (in prep for word2vec analysis) and stopwords (in prep for bag of words comparison between sightings). See "morefields_summaries_mongo.py" for the script.

The rest of the metadata was cleaned and expanded to include more fields. See "ufo_builddb.ipynb" for iPython notebook script.

Geocodes were done separately and in batches, so as not to exceed <b>Nominatim's</b> usage policy. See "geocode.py" for script.

Distance to nearest airport or military base was calculated for each sighting. See "airports.dat" (<a href = "http://openflights.org/data.html" target="_blank">source</a>) and "bases.js" (<a href = "http://empire.is/" target="_blank">source</a>) for data. Then used the Haversine formula to compute distance between sighting and all possible airports/military bases, and returned minimum distance for each one.

Census population data was combined to find population of location at time of sighting, and filter out non-US locations. See "1790-2010_MASTER.csv" for data. Source: U.S. <a href = "https://github.com/cestastanford/historical-us-city-populations" target="_blank">Census Bureau and Erik Steiner, Spatial History Project, Center for Spatial and Textual Analysis, Stanford University</a>. 

This resulted in 52,150 complete UFO sightings. See "52150_locations_USA_census_nonull.csv" for data.


###Code to analyze:

Found pairwise distances between all sightings, grouped them into components with <b>NetworkX</b> and binned datetime data to cluster sightings. Next, I assigned each sighting an index equal to the number of sightings within its componenet. This was coined its "credibility index". See "ufo_pairwisedist.ipynb" iPython notebook for script.

Then set up script to determine most similar UFO sighting to a given, new sighting. See "closest_sightings.py" for script.


###App

This script was eventually used to set up <a href = "http://ufosho.herokuapp.com" target="_blank">ufosho.herokuapp.com</a>, a tool to search for similar UFO sightings in time, location and written description. 


###Presentation

This project was presented on Sept 18, 2015 at Metis Data Science Bootcamp Career Day. The complete deck is <a href = "https://slides.com/claireger/ufo-sightings-credibility" target="_blank">here</a>.