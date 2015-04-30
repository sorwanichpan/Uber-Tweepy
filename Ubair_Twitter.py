#! /usr/bin/env python

# Make sure to pip install tweepy
__version__ = 0.1

import argparse, os
import oauth2 as oauth
import tweepy

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
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Return the API 
	return tweepy.API(auth)

def 

def main():
	# Set Global Variables and Get CLI Args
	define_GlobalVars()
	args = CLI_Arguments()

	# Get API Handler
	api = get_OAuth()





if __name__ == '__main__':
	main()