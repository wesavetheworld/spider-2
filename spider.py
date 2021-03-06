#!/bin/python

import sys
import os
import tweepy
import json
import codecs
import copy
import time



#	spider is a crawler for twitter
#	it uses the twitter api and keys generated by the user
#	
#	its function is to trap and save statuses that contain given keywords
#
#	it is dependent upon the existance of a file called "access_token.json" containing a json string of the user's access token
#	it takes two arguments:
#		1. the name of the file containing the keywords
#		2. the path to the directory where the generated files will be saved



def web_trap(word, path, statuses, check_set):

	text_file = codecs.open(path + word + '.txt', 'a', encoding='utf-8')
	json_file = open(path + word + '.json', 'a')

	reference = copy.deepcopy(check_set)	
	return_texts = set([])

	for status in statuses:

		if len(reference) >= 100:
			break

		text = ''.join(unicode(status['text']).splitlines()).replace('\t', ' ').replace('\n', ' ')

		if text not in reference:
	    
			json_obj = json.dumps(dict(copy.deepcopy(status)), encoding='utf-8')
			json_file.write(json_obj)
			text_file.write(text + '\n')
			return_texts.add(text)
			reference.add(text)

		else:
			pass

	return return_texts



def sleeper(mins):

	print 'waiting... 0 mins passed'

	timer = 0
	while timer < mins:
		time.sleep(60)
		timer += 1
		print 'waiting... ' + str(timer) + ' mins passed'



def main():

	# opens and reads user access token, and sets up access to twitter api

	AccessToken = json.loads(open('access_token.json', 'r').read())

	auth = tweepy.OAuthHandler(AccessToken['Consumer Key'],AccessToken['Consumer Secret'])
	auth.set_access_token(AccessToken['Access Token'], AccessToken['Access Token Secret'])
	twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

	# opens and reads the list of keywords

	keyword_file = sys.argv[1]
	keywords = open(keyword_file, 'r').read().split('\n')
	keywords.pop()

	outfile_path = sys.argv[2]

	# saves 100 statuses containing each keyword both as json objects and as one-line text statuses

	for keyword in keywords:

		text_file = codecs.open(outfile_path + keyword + '.txt', 'w', encoding='utf-8')
		json_file = open(outfile_path + keyword + '.json', 'w')
		text_file.close()
		json_file.close()

		POSTCOUNT = 0
		YEAR = 2017
		MONTH = 6
		DAY = 16		

		post_set = set([])

		while POSTCOUNT < 100:

			if MONTH < 10:
				MONTH_STR = '0' + str(MONTH)
			else:
				MONTH_STR = str(MONTH)
			if DAY < 10:
				DAY_STR = '0' + str(DAY)
			else:
				DAY_STR = str(DAY)
		
			SINCE_ID = str(YEAR) + '_' + MONTH_STR + '_' + DAY_STR
			
			try:
				status_list = twitter_api.search(q=keyword, lang='en', since_id=SINCE_ID, count=100)['statuses']
			except tweepy.TweepError as e:
				print str(e.reason)
				sleeper(15)
				status_list = twitter_api.search(q=keyword, lang='en', since_id=SINCE_ID, count=100)['statuses']
			new_texts = web_trap(keyword, outfile_path, status_list, post_set)

			if len(new_texts) > 0:

				post_set.update(new_texts)			
				print keyword + ': ' + str(len(new_texts))
				POSTCOUNT += len(new_texts)

			else:
				pass
				
			if DAY < 6:
				if MONTH == 1:
					MONTH = 12
				else:
					MONTH -= 1
			else:
				pass
			if DAY < 6:
				DAY = 28
			else:
				DAY -= 5



if __name__ == '__main__':
	main()
