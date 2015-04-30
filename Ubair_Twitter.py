#! /usr/bin/env python

# Make sure to pip install tweepy
__version__ = 0.1

import argparse, os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

# Override Tweepy Stream listener
class StdOutlistener(StreamListener):
	def on_status(self,status):
		if status.user.lang == "en":
			print "Tweet: ", status.text
			print "Timestamp: ",status.created_at
			print "Source: ",status.source
			print "Author: ",status.user.screen_name
	
			#  Geo Location checking
			if status.user.location is not None or status.user.location != " ":
				print "Location: ",status.user.location
			if status.place is not None:
				print "Place: ",status.place
				print "Coordinates: ",status.place.coordinates
			if status.user.geo_enabled is not True:
				if status.geo is not None and status.coordinates is not None:
					print "Coordinates: ",status.coordinates

			print "==================================="

	def on_error(self,status_code):
		if status_code == 200:
			print "Stream connection success! Status Code: {0}".format(status_code)
		elif status_code == 420:
			print "Stream rate limited! Disconnecting! Status Code: {0}".format(status_code)
			return False
		else: 
			print "Error Code: {0}".format(status_code)

def define_GlobalVars():
	global SCRIPTNAME
	global VERSION 
	SCRIPTNAME = os.path.splitext(os.path.basename(__file__))[0]
	VERSION = __version__

def CLI_Arguments():
	parser = argparse.ArgumentParser(
		description="Python Twitter Harvester",
		epilog="Sorasit Wanichpan 2015"
		)
	parser.add_argument('-v' , '--version', action='version', version='{s} {v}'.format(s = SCRIPTNAME ,v = VERSION))
	return parser.parse_args()

def get_OAuth():
	# Authentication Details
	consumer_key = ''
	consumer_secret = '' 
	access_token = ''
	access_token_secret = ''

	# Auth Token
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Return the API 
	return tweepy.API(auth)

def main():
	# Set Global Variables and Get CLI Args
	define_GlobalVars()
	args = CLI_Arguments()

	# Get API Handler and feed stream
	api = get_OAuth()
	myStream = Stream(api.auth,StdOutlistener())
	myStream.filter(track=['Uber'])
if __name__ == '__main__':
	main()