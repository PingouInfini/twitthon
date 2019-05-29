from kafka import KafkaProducer
import json
import logging
from time import sleep
from src import variables
import src.generators as generators

from argparse import ArgumentParser

parser = ArgumentParser(description='OpenALPR Python Test Program')

parser.add_argument("-v", "--verbosity", action="store_true", help="show debug logs")

options = parser.parse_args()


def main():
    try:
        logging.basicConfig(level=logging.INFO)
        if options.verbosity:
            logging.getLogger().setLevel(logging.DEBUG)

        logging.info(" Démarrage du generateur ")
        producer = KafkaProducer(bootstrap_servers='192.168.0.31:8092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        idbio="123456"
        tweet_directory= variables.outputtweet_user+"/bobjouy"
        media_directory= variables.outputmedia_user+"/bobjouy"
        logging.info("### Recuperation des tweet dans "+tweet_directory)
        logging.info("### Recuperation des medias dans "+media_directory)
        logging.info("### Envoi des tweets vers file kafka " + variables.topictweet_out)
        generators.raw_data_generator(variables.limit, tweet_directory, idbio, producer, variables.topictweet_out)
        logging.info("### Envoi des medias vers file kafka " + variables.topicmedia_out)
        generators.pictures_generator(variables.limit,media_directory, idbio, producer, variables.topicmedia_out)
        sleep(10)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin du generateur ")
    exit(0)

if __name__ == '__main__':
    main()