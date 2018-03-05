#!/usr/bin/env python3

import re
import os
import urllib.request
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
        self.profilePic = "https://twitter.com/" + \
            self.username + "/profile_image?size=original"

        # (Causes twitter to lock your account)
        #self.banner = user.profile_banner_url

        self.profilesPath = os.path.join(os.path.dirname(__file__), 'profiles')
        self.profilePath = os.path.join(self.profilesPath, self.username)

        if not os.path.isdir(self.profilesPath):
            os.mkdir(self.profilesPath)

    def write(self):
        print(self.username)
        print(self.name)
        print(self.description)
        print(self.tweetCount)
        print(self.following)

    def spoofProfile(self, api):
        # update fake profile from original
        if not os.path.isdir(self.profilePath):
            os.mkdir(self.profilePath)
        urllib.request.urlretrieve(
            self.profilePic, os.path.join(self.profilePath, 'profile.jpg'))

        api.update_profile(self.name, "", self.location, self.description)
        api.update_profile_image("profile.jpg")

        # api.update_profile_banner("banner.jpg")

    def getMentions(self, api):
        allTweets = ""
        mentionList = []
        public_tweets = api.user_timeline(screen_name=self.username, count=500)

        for tweet in public_tweets:  # get tweets
            allTweets += tweet.text

        for mention in allTweets.split(" "):
            if mention[:1] == "@":  # filter mentions
                mentionList.append(mention)
        countMention = Counter(mentionList)
        mentionList = countMention.most_common(5)  # top 5 mention list

        if not mentionList:  # if mention list is empty
            print("\n***********************")
            print("I couldn't find any account for spoofing")
            print("***********************")
        else:
            print("\nBest accounts for deceiving the target \n")
            print("***********************")
            for x in mentionList:
                print(colored(x[0] + str(" #" * x[1]), 'yellow'))
            print("***********************")

    def getTweets(self, api):
        print(colored("Collecting data...", 'yellow'))
        allTweets = ""
        public_tweets = api.user_timeline(screen_name=self.username, count=500)
        for tweet in public_tweets:  # get tweets
            tweet.text = re.sub(r"http\S+", "", tweet.text)  # remove URLs
            tweet.text = re.sub(r"RT", "", tweet.text)  # remote "RT" text
            tweet.text = re.sub(r'[\^@*][^\W]*', '', tweet.text)  # remove @

            allTweets += tweet.text
        return(allTweets)
