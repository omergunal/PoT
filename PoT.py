#MIT License

#Copyright (c) 2018 Ömer Günal

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import tweepy
import os
import sys
import argparse
from fake import Fake
from tweetGenerator import TweetGenerator
from termcolor import colored

consumer_key = "x"
consumer_secret = "x"
access_key = "x-x"
access_secret = "x"

def main():
	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_key, access_secret)
		auth.get_authorization_url()
		api = tweepy.API(auth)
	except tweepy.TweepError:
		print ('Error')

	username = sys.argv[1]
	user = api.get_user(username)


	target = Fake(user)
	target.getMentions(api)
	spoofAccount = input("Select account: ")
	url = input("Phishing URL: ")
	print("\n\n")

	spoofAc = Fake(api.get_user(spoofAccount))
	spoofAc.spoofProfile(api)

	tweets = spoofAc.getTweets(api)
	fakeTweetGenerator = TweetGenerator(tweets)
	fakeTweet = fakeTweetGenerator.setup(tweets)
	fakeTweet = ".@{} {} {} .".format(username,fakeTweet, url)

	print("\n***********************")
	print("This fake tweet has been sent:")
	print(colored(fakeTweet, 'green'))
	print("***********************")

	api.update_status(fakeTweet) # send tweet


if __name__ == "__main__":
	main()
