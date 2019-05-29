import logging
import threading
import base64
import os
import src.services as services
import src.variables as variables
import src.generators as generators
import src.producers as producers
from json import dumps
from kafka import KafkaProducer

class GeneratorMedia(threading.Thread):

    def __init__(self, account, idbio):
        threading.Thread.__init__(self)
        self.kafka_endpoint=variables.kafka_endpoint
        self.topicmedia_out=variables.topicmedia_out
        self.outputmedia_user=variables.outputmedia_user
        self.outputmedia_keywords=variables.outputmedia_keywords
        self.limit=variables.limit
        self.account=account
        self.idbio=idbio


    def run(self):
        logging.info("Lancement du thread pour remplir file kafka media")
        producer=KafkaProducer(bootstrap_servers=[self.kafka_endpoint], value_serializer=lambda x: dumps(x).encode('utf-8'),acks='all')
        media_directory= self.outputmedia_user+"/"+self.account
        logging.info("### Envoi des tweets vers file kafka " + self.topicmedia_out)
        generators.pictures_generator(self.limit,media_directory, self.idbio, producer, self.topicmedia_out)
        producer.close()

