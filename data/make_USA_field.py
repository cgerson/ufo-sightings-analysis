import pandas as pd
import reverse_geocoder as rg
import time

df_geocoded = pd.read_csv("83891_locations.csv")
del df_geocoded['Unnamed: 0']

def reverse_geocode_country(x):
    results = rg.search((x['lat'],x['long']))
    return results[0]['cc']

print "Start"
t = time.time()

df_geocoded['USA'] = df_geocoded.apply(reverse_geocode_country,axis=1)

t2 = t - time.time()
print "Finished in {} seconds".format(t2)
print "writing"

df_geocoded.to_csv("83891_locations_USA.csv",encoding='utf-8')
