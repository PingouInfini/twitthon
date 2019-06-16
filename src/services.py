import base64
import time
import logging
from json import dumps

import requests
from kafka import KafkaProducer
from tweepy import Cursor

import src.common.twitthon_acquisition
import src.common.twitthon_authentication
import src.producers as producers


def get_accounts_from_user(user):
    api = src.common.twitthon_authentication.get_api()
    results = api.search_users(q=user)

    accounts = []
    for result in results:
        accounts.append(result._json['screen_name'])

    logging.info("Compte(s) trouve(s) pour '" + str(user) + "' : " + str(accounts))
    return accounts


def get_user_tweet_and_push_forward(idbio, account, limit, kafka_endpoint, topic_tweet, topic_media):
    index_m = 0
    api = src.common.twitthon_authentication.get_api()
    if account != "":
        min_id = 9999999999999999999
        # get first 100 tweets from user
        nb_tweet_getted = 0
        total_tweet_getted = 0
        total_media_getted = 0

        producer = KafkaProducer(bootstrap_servers=[kafka_endpoint],
                                 value_serializer=lambda x: dumps(x).encode('utf-8'))

        # récupération des 100er tweets...
        for page in Cursor(api.user_timeline, screen_name=account, count=100).pages(1):
            for status in page:
                tweet = status._json
                nb_tweet_getted += 1
                if (int(tweet['id_str']) < min_id):
                    min_id = int(tweet['id_str'])

                # pousser le tweet (+ media) dans les topics:
                producers.fill_kafka_tweet_idbio(tweet, idbio, producer, topic_tweet)
                media = extract_media_from_tweet(tweet)
                if media is not None:
                    total_media_getted += 1
                    producers.fill_kafka_picture_idbio(media, idbio, producer, topic_media)

        total_tweet_getted += nb_tweet_getted


        # get next 100 if exists
        while (nb_tweet_getted > 0):

            if (total_tweet_getted > int(limit)) and int(limit) != 0:
                logging.info("LIMITE ATTEINTE !!!")
                break

            nb_tweet_getted = 0
            for page in Cursor(api.user_timeline, screen_name=account, count=100, max_id=min_id).pages(1):
                for status in page:
                    tweet = status._json
                    if (int(tweet['id_str']) != min_id):
                        nb_tweet_getted += 1
                        if (int(tweet['id_str']) < min_id):
                            min_id = int(tweet['id_str'])
                        # pousser le tweet (+ media) dans les topics:
                        producers.fill_kafka_tweet_idbio(tweet, idbio, producer, topic_tweet)
                        media = extract_media_from_tweet(tweet)
                        if media is not None:
                            total_media_getted += 1
                            producers.fill_kafka_picture_idbio(media, idbio, producer, topic_media)
            total_tweet_getted += nb_tweet_getted



def extract_media_from_tweet(tweet):
    try:
        index = 0
        for media in tweet['entities']['media']:
            index += 1

            r = requests.get(media['media_url'], allow_redirects=True)

            if (media['type'] == "photo"):
                extension = "image/jpg"
                image = r.content
            # TODO pour plus tard ... (gestion des medias video et gif)
            # elif (media['type'] == "video" or media['type'] == "animated_gif"):
            #     filename += ".mp4"
            #     io.open(filename, 'wb').write(r.content)

            media = {
                'name': str(tweet['id']) + "_" + str(index),
                'extension': extension,
                'image': base64.b64encode(bytearray(image)).decode('UTF-8')
            }

            return media
    except:
        return None


def get_user_tweet(user,
                   limit=500,
                   outputtweet="timeline/json",
                   outputmedia="timeline/media"):
    api = src.common.twitthon_authentication.get_api()
    src.common.twitthon_acquisition.get_user_tweet(api, user, limit, outputtweet, outputmedia)


def get_tweet_from_keywords(keywords,
                            limit=500,
                            outputtweet="keywords/json",
                            outputmedia="keywords/media"):
    api = src.common.twitthon_authentication.get_api()
    src.common.twitthon_acquisition.get_tweet_from_keywords(api, keywords, limit, outputtweet, outputmedia)
