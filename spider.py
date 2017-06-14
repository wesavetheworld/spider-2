#!/bin/python

import sys
import os
import twitter
import tweepy
import json
import codecs



#	spider is a crawler for twitter
#	it uses the twitter api and keys generated by the user
#	
#	its function is to trap and save statuses that contain given keywords
#
#	it is dependent upon the existance of a file called "access_token.json" containing a json string of the user's access token
#	it takes two arguments:
#		1. the name of the file containing the keywords
#		2. the path to the directory where the generated files will be saved



def web_trap(word, path, API):

	text_file = codecs.open(path + keyword + '.txt', 'w', encoding='utf-8')
	json_file = open(path + keyword + '.json', 'w')

	statuses = API.search(keyword)['statuses']
	
	for status in statuses:

		json_obj = json.dump(status, json_file)

		text = ''.join(unicode(status['text']).splitlines()).replace('\t', ' ').replace('\n', ' ')
		text_file.write(text + '\n')



def main():

	# opens and reads user access token, and sets up access to twitter api

	AccessToken = json.loads(open('access_token.json', 'r').read())

	auth = tweepy.OAuthHandler(AccessToken['Consumer Key'],AccessToken['Consumer Secret'])
	auth.set_access_token(AccessToken['Access Token'], AccessToken['Access Token Secret'])
	twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

	# opens and reads the list of keywords

	keyword_file = sys.argv[1]
	keywords = open(keyword_file, 'r').read().split('\n')

	outfile_path = sys.argv[2]

	# saves 100 statuses containing each keyword both as json objects and as one-line text statuses

	for keyword in keywords:

		web_trap(keyword, outfile_path, twitter.api)



if __name__ == '__main__':
	main()
