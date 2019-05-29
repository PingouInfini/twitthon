#!/usr/bin/env python
import logging
import multiprocessing
import json
import src.services as services
import src.variables as variables
import src.generators as generators
from json import dumps

from kafka import KafkaConsumer, KafkaProducer

class Consumer(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.kafka_endpoint=variables.kafka_endpoint
        self.topic_in=variables.topic_in
        self.topictweet_out=variables.topictweet_out
        self.topicmedia_out=variables.topicmedia_out
        self.outputtweet_user=variables.outputtweet_user
        self.outputmedia_user=variables.outputmedia_user
        self.outputtweet_keywords=variables.outputtweet_keywords
        self.outputmedia_keywords=variables.outputmedia_keywords
        self.limit=variables.limit


    def stop(self):
        self.stop_event.set()

    def run(self):
        logging.info("Lancement du thread pour depiler file kafka "+self.topic_in)
        consumer = KafkaConsumer(bootstrap_servers=self.kafka_endpoint,
                                 auto_offset_reset='latest',
                                 consumer_timeout_ms=1000)
        producer=KafkaProducer(bootstrap_servers=[self.kafka_endpoint], value_serializer=lambda x: dumps(x).encode('utf-8'))

        consumer.subscribe([self.topic_in])

        while not self.stop_event.is_set():
            for message in consumer:
                #decodage du message en byte to string
                msg = message.value.decode('utf8')
                #recuperation des donneés du json
                data = json.loads(msg)
                idbio = data['idBio']
                nom = data['nom']
                prenom = data ['prenom']
                if self.stop_event.is_set():
                    break
                user =prenom + " "+ nom
                accounts = services.get_accounts_from_user(user)
                if len(accounts) > 0:
                    # Get the first account, then get tweets
                    account = accounts[0]

                    logging.info("### Récupération des tweets du compte : "+str(account))
                    services.get_user_tweet(account,self.limit, self.outputtweet_user, self.outputmedia_user)
                    logging.info("### Récupération des tweets mentionnant le compte : "+str(account))
                    services.get_tweet_from_keywords(account,self.limit, self.outputtweet_keywords, self.outputmedia_keywords)
                    logging.info("### Récupération des tweets mentionnant l'utilisateur : "+str(user))
                    services.get_tweet_from_keywords(user,self.limit, self.outputtweet_keywords, self.outputmedia_keywords)
                    tweet_directory= self.outputtweet_user+"/"+str(account)
                    media_directory= self.outputmedia_user+"/"+str(account)
                    logging.info("### Envoi des tweets vers file kafka " + self.topictweet_out)
                    generators.raw_data_generator(tweet_directory, idbio, producer, self.topictweet_out)
                    logging.info("### Envoi des medias vers file kafka " + self.topicmedia_out)
                    generators.pictures_generator(media_directory, idbio, producer, self.topicmedia_out)

        consumer.close()
