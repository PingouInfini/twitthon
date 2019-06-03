import logging
import threading
import src.services as services
import src.variables as variables
import src.generators as generators
from json import dumps
from kafka import KafkaProducer

class GeneratorTweet(threading.Thread):

    def __init__(self, account, idbio):
        threading.Thread.__init__(self)
        self.kafka_endpoint=variables.kafka_endpoint
        self.topictweet_out=variables.topictweet_out
        self.topictweet_outdeux=variables.topictweet_outdeux
        self.outputtweet_user=variables.outputtweet_user
        self.outputtweet_keywords=variables.outputtweet_keywords
        self.limit=variables.limit
        self.account=account
        self.idbio=idbio

    def run(self):
        logging.info("Lancement du thread pour remplir file kafka tweet")
        producer=KafkaProducer(bootstrap_servers=[self.kafka_endpoint], value_serializer=lambda x: dumps(x).encode('utf-8'))
        tweet_directory= self.outputtweet_user+"/"+self.account
        logging.info("### Envoi des tweets vers file kafka " + self.topictweet_out)
        generators.raw_data_generator(self.limit,tweet_directory, self.idbio, producer, self.topictweet_out)
        logging.info("### Envoi des tweets vers file kafka " + self.topictweet_outdeux)
        generators.raw_data_generator(self.limit,tweet_directory, self.idbio, producer, self.topictweet_outdeux)
        producer.close()