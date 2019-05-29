#!/usr/bin/env python
import logging
import threading
import json
import src.services as services
import src.variables as variables
import src.generatormedia as generatormedia
import src.generatortweet as generatortweet


from kafka import KafkaConsumer, KafkaProducer

class Consumer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.kafka_endpoint=variables.kafka_endpoint
        self.topic_in=variables.topic_in
        self.topictweet_out=variables.topictweet_out
        self.topicmedia_out=variables.topicmedia_out
        self.outputtweet_user=variables.outputtweet_user
        self.outputmedia_user=variables.outputmedia_user
        self.outputtweet_keywords=variables.outputtweet_keywords
        self.outputmedia_keywords=variables.outputmedia_keywords
        self.limit=variables.limit


    def run(self):
        logging.info("Lancement du thread pour depiler file kafka "+self.topic_in)
        consumer = KafkaConsumer(bootstrap_servers=self.kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([self.topic_in])
        for message in consumer:
            #recuperation des data du json du message
            idbio = message.value['idBio']
            nom = message.value['nom']
            prenom = message.value ['prenom']
            user =prenom + " "+ nom
            accounts = services.get_accounts_from_user(user)
            if len(accounts) > 0:
                # Get the first account, then get tweets
                account = accounts[0]
                logging.info("### Récupération des " +self.limit+" tweets du compte : "+str(account))
                services.get_user_tweet(account,self.limit, self.outputtweet_user, self.outputmedia_user)
                #logging.info("### Récupération des tweets mentionnant le compte : "+str(account))
                #services.get_tweet_from_keywords(account,self.limit, self.outputtweet_keywords, self.outputmedia_keywords)
                #logging.info("### Récupération des tweets mentionnant l'utilisateur : "+str(user))
                #services.get_tweet_from_keywords(user,self.limit, self.outputtweet_keywords, self.outputmedia_keywords)
                tasks = [
                    generatormedia.GeneratorMedia(str(account),idbio),
                    generatortweet.GeneratorTweet(str(account),idbio)
                ]
                for t in tasks:
                    t.start()

                for t in tasks:
                    t.join()

        consumer.close()
