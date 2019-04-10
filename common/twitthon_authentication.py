import tweepy
import os

def get_api():
    # get_credentials_from_file (used for twitter connection)
    consumer_key, consumer_secret, access_key, access_secret = get_credentials_from_file()
    return init_tweepy(consumer_key, consumer_secret, access_key, access_secret)


def get_credentials_from_file():
    f = open(os.path.dirname(os.path.realpath(__file__))+"/../twitter_credentials.txt", "r")

    lines = f.readlines()
    consumer_key = str(lines[1]).replace("\n", "")
    consumer_secret = str(lines[2]).replace("\n", "")
    access_key = str(lines[3]).replace("\n", "")
    access_secret = str(lines[4]).replace("\n", "")
    f.close()
    return consumer_key, consumer_secret, access_key, access_secret


def init_tweepy(consumer_key, consumer_secret, access_key, access_secret):
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)
