import config
import datetime
from geopy.geocoders import Nominatim
import tweepy

def unique(list1):
	list_set = set(list1)
	unique_list = (list(list_set)) 
	return unique_list

def countries(handle):

	try:
		userHandle = handle

		auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
		auth.set_access_token(config.access_token, config.access_token_secret)
		api = tweepy.API(auth)

		tweets = api.user_timeline(screen_name=userHandle, count=100, include_rts = False, tweet_mode = 'extended')

		places = []
		geolocator = Nominatim(user_agent="Twitter Bot", timeout=3) 

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
		
	except GeocoderTimedOut:
		return countries(handle)
		
handle = "jk_rowling"
print(countries(handle))