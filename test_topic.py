#!/usr/bin/env python
import logging
import threading
import json
import src.variables as variables



from kafka import KafkaConsumer, KafkaProducer

#pour tester ce qu'il y a dans la file kafka self.topic_in

class ConsumerNER(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.kafka_endpoint=variables.kafka_endpoint
        self.topic_in="textToNER"


    def run(self):
        logging.info("Lancement du thread pour depiler file kafka "+self.topic_in)
        consumer = KafkaConsumer(bootstrap_servers=self.kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='earliest')

        consumer.subscribe([self.topic_in])
        for message in consumer:
            #recuperation des data du json du message
            idbio = message.value['idBio']
            tweet = message.value['tweet']

        consumer.close()

if __name__ == '__main__':
    tasks = [
        ConsumerNER()
    ]
    #lancement du thread de consomation du topic
    for t in tasks:
        t.start()
