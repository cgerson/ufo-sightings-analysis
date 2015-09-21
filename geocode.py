import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim()

df = pd.read_csv("19120_not_geocoded.csv") #or any csv of sightings, with fields 'city' and 'state'
df = df.ix[:1000] #1000 locations at a time
df['FullLocation'] = df.city.map(str) + ", " + df.state.map(str)

print "About to geocode"

for index, row in df.iterrows():
    try:
        location = geolocator.geocode(row['FullLocation'], timeout=60)
        lat = location.latitude
        lon = location.longitude
    except AttributeError:
        lon = 0
        lat = 0
    df.loc[index,'lon'] = lon
    df.loc[index,'lat'] = lat
    print str(index)

df.to_csv("0_1000_geocoded.csv",encoding="utf-8") #write to csv file
