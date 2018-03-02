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

import re
import os
from collections import Counter
from termcolor import colored

class Fake():
# fake human class
	def __init__(self, user):
		self.username = user.screen_name
		self.name = user.name
		self.description = user.description
		self.tweetCount = str(user.statuses_count)
		self.following = str(user.friends_count)
		self.followers = str(user.followers_count)
		self.favs = str(user.favourites_count)
		self.website = str(user.url)
		self.created = str(user.created_at)
		self.location = user.location
		self.lang = user.lang
		self.profilePic = "https://twitter.com/" + user.screen_name + "/profile_image?size=original"
		#self.banner = user.profile_banner_url

	def write(self):
		print(self.username)
		print(self.name)
		print(self.description)
		print(self.tweetCount)
		print(self.following)
		#print(self.banner)

	def spoofProfile(self, api):
		# update fake profile from original
		os.system("wget -O profile.jpg "+ "https://twitter.com/"+self.username+"/profile_image?size=original")
	#	os.system("wget -O banner.jpg " + self.banner)
		api.update_profile(self.name, "", self.location, self.description)
		api.update_profile_image("profile.jpg")
	#	api.update_profile_banner("banner.jpg")

	def getMentions(self, api):
		allTweets = ""
		mentionList = []
		public_tweets = api.user_timeline(screen_name = self.username,count = 500)

		for tweet in public_tweets: # get tweets
			allTweets += tweet.text

		for mention in allTweets.split(" "):
			if mention[:1] == "@": #filter mentions
                               mentionList.append(mention)
		countMention = Counter(mentionList)
		mentionList = countMention.most_common(5) # top 5 mention list

		if not mentionList: # if mention list is empty
			print("\n***********************")
			print("I couldn't find any account for spoofing")
			print("***********************")
		else:
			print("\nBest accounts for deceiving the target \n")
			print("***********************")
			for x in mentionList:
				print(colored(x[0] + str(" #"*x[1]), 'yellow'))
			print("***********************")

	def getTweets(self, api):
		print(colored("Collecting data...", 'yellow'))
		allTweets = ""
		public_tweets = api.user_timeline(screen_name = self.username,count = 500)
		for tweet in public_tweets: # get tweets
			tweet.text = re.sub(r"http\S+", "", tweet.text) # remove URLs
			tweet.text = re.sub(r"RT", "", tweet.text) # remote "RT" text
			tweet.text = re.sub(r'[\^@*][^\W]*', '', tweet.text) # remove @

			allTweets += tweet.text
		return(allTweets)
