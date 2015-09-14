import sys
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
from sklearn.feature_extraction.text import TfidfVectorizer
from geopy.geocoders import Nominatim
geolocator = Nominatim(country_bias="US") #hopefully runs faster with country bias


#import text2num

sys.path.insert(0, '../ufo-sightings-data/')
from morefields_summaries_mongo import summary_to_list

#connect to Mongo
client = MongoClient(host="54.69.198.239",port=27017)
db = client.UFO
col = db.Summaries

#collect arguments
dt = sys.argv[1]
location = sys.argv[2]
summary = sys.argv[3]

def check_location(location = location):
    try:
        geo = geolocator.geocode(location, timeout=60).raw
        return location
    except:
        print ("You entered " + location) 
        new_location = input("Please enter a valid location (City, ST): ")
        print ("You entered " + new_location)
        return check_location(location = new_location)

location_checked = check_location()

print
print "Finding similar sighting with parameters:"
print dt
print location
print summary

#load csvs
df_sightings = pd.read_csv("52150_reliability_count.csv")
cities = pd.read_csv("4945_dist_comp.csv")

def to_seconds(x):
    t = datetime(1900,1,1)
    try:
        return (parser.parse(x) - t).total_seconds()
    except:
        return (x-t).total_seconds()

def date_to_seconds(x):
    date_object = datetime.strptime(x, '%m/%d/%Y %H:%M')
    seconds = to_seconds(date_object)
    return seconds

def location_to_comp(x):
    if x in cities.CityST.values: #if location already in df. change this to hash lookup
        lat = cities[cities['CityST']==x].lat.values[0]
        lon = cities[cities['CityST']==x].lon.values[0]
    else:
        geo = geolocator.geocode(x, timeout=60)
        lat = geo.latitude
        lon = geo.longitude
            
    d = pairwise_distances(cities[['lon','lat']],(lon,lat))
            
    return cities.ix[np.argmin(d)]['dist_comp']
    
def return_links(dt = dt, location = location_checked, time = 45000):
    subset_time = df_sightings[abs(df_sightings['seconds']-date_to_seconds(dt))<time] #45000 within 12 hours
    subset_timedist = subset_time[subset_time['dist_comp']==int(location_to_comp(location))]

    links = subset_timedist.link_no_ext.values
    fixed_links = [elem[1:] if len(elem)>10 else elem for elem in list(links)] #didn't save link name correctly

    if len(fixed_links)>0:
        return fixed_links,subset_timedist
    else:
        print time
        time += 45000
        return return_links(time=time)

def mongo_summaries():
    bow = []
    text = []
    links,_ = return_links()
    for i in col.find({"link" : {"$in": list(links)}}):
        stemmed_words = []
        words = i['bag_of_words'][0].split()
        for w in words:
            stemmed_words.append(porter_stemmer.stem(w))
        bow.append(" ".join(stemmed_words))
        text.append(i['text'])
    
    return bow,text

def vector_analysis(summary = summary):
    bow,text = mongo_summaries()
    _,df = return_links()

    df=df.reset_index() #to be able to grab values by index
    
    vectorizer_tf = TfidfVectorizer(stop_words = "english")
    X = vectorizer_tf.fit_transform(bow)

    t = summary_to_list(summary)

    print t
    
    t_stem = []
    stemmed_words = []
    for w in t:
        stemmed_words.append(porter_stemmer.stem(w))
    t_stem.append(" ".join(stemmed_words))
    
    X_new = vectorizer_tf.transform(t_stem)

    print "Distance",pairwise_distances(X,X_new)

    for elem in np.argsort(pairwise_distances(X,X_new),axis=None): #in case closest match is empty
        if text[elem]:
            closest = text[elem]
            index = elem
            break
        else:
            continue

    #print summary of most similar sighting
    print "City",df.ix[index]['CityST'].values[0]
    print "Date",df.ix[index]['date_datetime'].values[0]
    print "Shape",df.ix[index]['shape'].values[0]
    print "Duration (in sec)",df.ix[index]['duration_seconds'].values[0]
    
    #return text[np.argmin(pairwise_distances(X,X_new))]
    return closest

print vector_analysis()
