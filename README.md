# ufo-sightings-analysis

This repo holds my code and methods for an analysis of UFO sightings reports in the US. Raw data can be found at NUFORC's online <a href = "http://www.nuforc.org/webreports.html" target="_blank">UFO sightings database</a>.

###Code to collect:

I used the "wget" command to scrape 99,477 UFO sightings descriptions (summaries) from the NUFORC site. Essentially followed <a href = "http://blog.scotterussell.com/post/93524577748/ufo-data-science-how-we-get-data-part-2" target="_blank">this tutorial</a>.

Once all summaries were downloaded on my remote server, I used <b>BeautifulSoup</b> to scrape the relevant information and insert one by one in my <b>MongoDB</b> database. See "build_summaries.py" for the script.

The rest of the metadata of each UFO sighting (timestamp, location, duration and shape) were scraped and stored in a pandas dataframe, with the link to the sighting as it's unique ID. See "ufo_nosummary.pkl" for the data.


###Code to clean:

The summaries were filtered and stripped of punctuation (in prep for word2vec analysis) and stopwords (in prep for bag of words comparison between sightings). See "morefields_summaries_mongo.py" for the script.

The rest of the metadata was cleaned and expanded to include more fields. See "ufo_builddb.ipynb" for iPython notebook script.

Geocodes were done separately and in batches, so as not to exceed Nominatim's usage policy. See "geocode.py" for script.

Census population data was combined to find population of location at time of sighting, and filter out non-US locations. See "1790-2010_MASTER.csv" for data. Source: U.S. <a href = "https://github.com/cestastanford/historical-us-city-populations" target="_blank">Census Bureau and Erik Steiner, Spatial History Project, Center for Spatial and Textual Analysis, Stanford University</a>. 

This resulted in 52,150 complete UFO sightings. See "52150_locations_USA_census_nonull.csv" for data.

###Code to analyze:

Found pairwise distance between all sightings and binned datetime data to cluster sightings. See "ufo_pairwisedist.ipynb" iPython notebook for script.

Then set up script to determine most similar UFO sighting to a given, new sighting. See "closest_sightings.py" for script. This script was eventually used to set up ufosho.herokuapp.com, a tool to search for similar UFO sightings in time, location and written description. 
