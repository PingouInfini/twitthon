import os
import io
import json
import requests
from tweepy import Cursor

def get_user_tweet(api, account, limit, outputtweet, outputmedia):
    if account != "":
        min_id = 9999999999999999999
        # get first 100 tweets from user
        nb_tweet_getted = 0
        total_tweet_getted = 0

        for page in Cursor(api.user_timeline, screen_name=account, count=100).pages(1):
            for status in page:
                tweet = status._json
                nb_tweet_getted += 1
                if( int(tweet['id_str']) < min_id ):
                    min_id = int(tweet['id_str'])
                save_1_tweet(outputtweet,
                             outputmedia,
                             account,
                             tweet, tweet['id_str'])
        total_tweet_getted += nb_tweet_getted
        print(str(nb_tweet_getted)+"/"+str(total_tweet_getted))

        #get next 100 if exists
        while(nb_tweet_getted > 0):

            if(total_tweet_getted > int(limit)) and  limit!=0 :
                print("LIMITE ATTEINTE !!!")
                break

            nb_tweet_getted = 0
            for page in Cursor(api.user_timeline, screen_name=account, count=100,max_id=min_id).pages(1):
                for status in page:
                    tweet = status._json
                    if(int(tweet['id_str']) != min_id):
                        nb_tweet_getted += 1
                        if( int(tweet['id_str']) < min_id ):
                            min_id = int(tweet['id_str'])
                        save_1_tweet(outputtweet,
                                     outputmedia,
                                     account,
                                     tweet, tweet['id_str'])
            total_tweet_getted += nb_tweet_getted
            print(str(nb_tweet_getted)+"/"+str(total_tweet_getted))


def get_tweet_from_keywords(api, keywords, limit, outputtweet, outputmedia):
    total_tweet_getted = 0
    last_id = -1

    if keywords != "":
        q_keywords = "\"" + keywords + "\""

        while total_tweet_getted < int(limit):
            count = int(limit) - total_tweet_getted
            try:
                new_tweets = api.search(q=q_keywords, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    break
                for status in new_tweets:
                    tweet = status._json
                    total_tweet_getted += 1
                    save_1_tweet(outputtweet,
                                 outputmedia,
                                 keywords,
                                 tweet, tweet['id_str'])
                last_id = new_tweets[-1].id
            except Exception as e:
                print(e)
                break


def save_1_tweet(jsonoutput, mediaoutput, account, tweet, id_str):
    json_path = os.path.join(jsonoutput,account)
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    with io.open(json_path + '/' + id_str + '.json', 'w', encoding='utf-8') as jfile:
        jfile.write(json.dumps(tweet, ensure_ascii=False))

    media_path = os.path.join(mediaoutput,account)
    if not os.path.exists(media_path):
        os.makedirs(media_path)
    save_tweet_media(tweet, media_path)


def save_tweet_media(tweet, media_path):
    try:
        index = 0
        for media in tweet['entities']['media']:
            index += 1

            r = requests.get(media['media_url'], allow_redirects=True)
            filename = media_path + "/" + str(tweet['id']) + "_" + str(index)
            if (media['type'] == "photo"):
                filename += ".jpg"
                io.open(filename, 'wb').write(r.content)
            elif (media['type'] == "video" or media['type'] == "animated_gif"):
                filename += ".mp4"
                io.open(filename, 'wb').write(r.content)
    except:
        pass
