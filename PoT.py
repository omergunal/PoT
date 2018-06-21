#!/usr/bin/env python3


import tweepy
import os
import argparse
import configparser
from fake import Fake
from tweetGenerator import TweetGenerator
from termcolor import colored

hardreturn = '\n'
que = colored('[?] ', 'blue')
bad = colored('[-] ', 'red')
good = colored('[+] ', 'green')
run = colored('[~] ', 'yellow')

def CreateProfile(name):
    f = open(name, 'w+');
    f.write('[twitter_api]\n')
    f.write('consumer_key = ' + input("Consumer Key: ") + ' \n')
    f.write('consumer_secret = ' + input("Consumer Secret: ") + ' \n')
    f.write('access_token_key = ' + input("Access Token Key: ") + ' \n')
    f.write('access_token_secret = ' + input("Access Token Secret: ") + ' \n')
    print("Config file created, please restart the program.")

def main():
    try:
        config_profile = ''
        config = configparser.RawConfigParser()
        config_profile = input("What is the name of the profile you want to use?:")
        config_profile += '.cfg'
        config.read(os.path.join(os.path.dirname(__file__), config_profile))
        try:
            consumer_key = config.get('twitter_api', 'consumer_key')
            consumer_secret = config.get('twitter_api', 'consumer_secret')
            access_token_key = config.get('twitter_api', 'access_token_key')
            access_token_secret = config.get('twitter_api', 'access_token_secret')
        except configparser.Error as e:
            print(bad + str(e))
            CreateProfile(config_profile)
            exit(1)

        parser = argparse.ArgumentParser(description='Phishing on Twitter')
        parser.add_argument('-u', '--username', help='username to phish with ')
        args = parser.parse_args()

        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token_key, access_token_secret)
            auth.get_authorization_url()
            api = tweepy.API(auth)
        except tweepy.TweepError:
            print(bad + 'Authentication Error')
            exit(1)

        if args.username:
            username = args.username
        else:
            print("There is a mistake about username")
        user = api.get_user(username)

        target = Fake(user)
        target.getMentions(api)
        spoofAccount = input(que + "Select account: ")
        url = input(que + "Phishing URL: ")
        print(hardreturn * 2)

        spoofAc = Fake(api.get_user(spoofAccount))
        spoofAc.spoofProfile(api)

        tweets = spoofAc.getTweets(api)
        fakeTweetGenerator = TweetGenerator(tweets)
        fakeTweet = fakeTweetGenerator.setup(tweets)
        fakeTweet = ".@{} {} {} .".format(username, fakeTweet, url)

        print(hardreturn)
        print("***********************")
        print("This fake tweet has been sent:")
        print(colored(fakeTweet, 'green'))
        print("***********************")

        api.update_status(fakeTweet)  # send tweet
    except Exception as e:
        print(bad + str(e))


if __name__ == "__main__":
    main()
