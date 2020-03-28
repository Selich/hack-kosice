consumer_key = "OYSPnW2fP34yd3Phbvw4yQozk"
consumer_secret = "15VHmSXkoku7FTz4VBuVfwjtVVf9QxIpRzxjociEUK0jeebROu"
access_token = "990891304367411201-Ew2E3LGE5dXnuwBxFxDXmZmfIdr1MIO"
access_token_secret = "7LB5ZPF7LSbxmoC99ERIYiYDLgPT04sQbyh4ggddXpZwP"

import tweepy
import datetime
from geopy.geocoders import Nominatim

def unique(list1):
	list_set = set(list1)
	unique_list = (list(list_set)) 
	return unique_list

def countries(handle):

	userHandle = handle

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	tweets = api.user_timeline(screen_name=userHandle, count=100, include_rts = False, tweet_mode = 'extended')

	places = []
	geolocator = Nominatim(user_agent="Twitter Bot") 

	for tweet in tweets:
		if ((datetime.datetime.now() - tweet.created_at).days < 15):
			if (tweet.place != None):
				coordinates = geolocator.geocode(tweet.place.full_name)
				location = geolocator.reverse("{}, {}".format(coordinates.latitude, coordinates.longitude), exactly_one=True)
				address = location.raw['address']
				places.append(address.get('country', ''))
			else:
				coordinates = geolocator.geocode(tweet.user.location)
				location = geolocator.reverse("{}, {}".format(coordinates.latitude, coordinates.longitude), exactly_one=True)
				address = location.raw['address']
				places.append(address.get('country', ''))
		else:
			break

	countries = unique(places)
	return countries