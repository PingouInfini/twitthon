import os
import io
import json
import requests
from tweepy import Cursor



def get_user_tweet(api, user, limit, outputtweet, outputmedia):
    if user != "":
        pages = (limit // 200) + 1
        for page in Cursor(api.user_timeline, screen_name=user, count=200).pages(pages):
            for status in page:
                tweet = status._json
                save_1_tweet(outputtweet,
                             outputmedia,
                             tweet, tweet['id_str'])


def get_tweet_from_keywords(api, keywords, limit, outputtweet, outputmedia):
    if keywords != "":
        keywords = "\"" + keywords + "\""
        pages = (limit // 200) + 1
        for page in Cursor(api.search, q=keywords, count=200).pages(pages):
            for status in page:
                tweet = status._json
                save_1_tweet(outputtweet,
                             outputmedia,
                             tweet, tweet['id_str'])



def save_1_tweet(jsonoutput, mediaoutput, tweet, id_str):
    if not os.path.exists(jsonoutput):
        os.makedirs(jsonoutput)
    with io.open(jsonoutput + '/' + id_str + '.json', 'w', encoding='utf-8') as jfile:
        jfile.write(json.dumps(tweet, ensure_ascii=False))
    if not os.path.exists(mediaoutput):
        os.makedirs(mediaoutput)
    save_tweet_media(tweet, mediaoutput)


def save_tweet_media(tweet, mediaoutput):
    try:
        index = 0
        for media in tweet['entities']['media']:
            index += 1

            r = requests.get(media['media_url'], allow_redirects=True)
            filename = mediaoutput + "/" + str(tweet['id']) + "_" + str(index)
            if (media['type'] == "photo"):
                filename += ".jpg"
                io.open(filename, 'wb').write(r.content)
            elif (media['type'] == "video" or media['type'] == "animated_gif"):
                filename += ".mp4"
                io.open(filename, 'wb').write(r.content)
    except:
        pass
