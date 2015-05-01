#! /usr/bin/env python

# Make sure to pip install tweepy
__version__ = 0.1

import argparse, os, sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
from elasticsearch import Elasticsearch
import requests
import nltk

# Override Tweepy Stream listener
class StdOutlistener(StreamListener):

	def on_status(self,status):
		es = Elasticsearch()
		jsonDict = dict()
		if status.user.lang == "en":

			jsonDict['Timestamp'] = status.created_at
			jsonDict['Tweet'] = status.text
			jsonDict['Source'] = status.source
			jsonDict['Author'] = status.user.screen_name 
			jsonDict['ID'] = status.id

			token = nltk.word_tokenize(status.text)
			mood = nltk.pos_tag(token)
	
			#  Geo Location checking
			if not status.user.location and len(status.user.location) == 0:
				jsonDict['Location'] = status.user.location
				#print "Location: ",status.user.location
			# if status.place is not None:
			# 	jsonDict['Place'] = status.place
			# 	jsonDict['Coordinates'] = status.coordinates
				# print "Place: ",status.place
				# print "Coordinates: ",status.coordinates
			# if status.user.geo_enabled is not True:
			# 	if status.geo is not None and status.coordinates is not None:
			# 		print "Coordinates: ",status.coordinates

			# print "==================================="
			# res = es.index(index="test-index", doc_type='tweet', id=jsonDict['ID'], body=jsonDict)
			# es.indices.refresh(index="test-index")
			print "ID: ", status.id
			print "Tweet: ", status.text

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
	myStream.filter(track=['Uber','Lyft'])
if __name__ == '__main__':
	main()