import re
import os
from collections import Counter

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
		self.profilePic = "https://twitter.com/"+user.screen_name+"/profile_image?size=original"
		#self.banner = user.profile_banner_url

	def write(self):
		print(self.username)
		print(self.name)
		print(self.description)
		print(self.tweetCount)
		print(self.following)
		print(self.banner)

	def spoofProfile(self, api):
		# update fake profile from original
		os.system("wget -O profile.jpg "+ "https://twitter.com/"+self.username+"/profile_image?size=original")
		#os.system("wget -O banner.jpg " + self.banner)
		api.update_profile(self.name, "", self.location, self.description)
		api.update_profile_image("profile.jpg")
		#api.update_profile_banner("banner.jpg")

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
		print("Best accounts for deceiving the target")
		print("***********************")
		print(countMention.most_common(5))
		print("***********************")
		print(allTweets)

	def getTweets(self, api):
		allTweets = ""
		public_tweets = api.user_timeline(screen_name = self.username,count = 500)
		for tweet in public_tweets: # get tweets
			tweet.text = re.sub(r"http\S+", "", tweet.text) # remove URLs
			tweet.text = re.sub(r"RT", "", tweet.text) # remote "RT" text
			tweet.text = re.sub(r'[\^@*][^\W]*', '', tweet.text) # remove @

			print(tweet.text)
			allTweets += tweet.text
