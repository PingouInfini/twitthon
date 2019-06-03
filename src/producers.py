#pour envoyer dans une file kafka un tweet avec un bioId
def fill_kafka_tweet_idbio(json, bio_id, producer, topic):
    #construction du json
    tweet_idbio = {
        "idBio": bio_id,
        "tweet": json
    }

    producer.send(topic, value=(tweet_idbio))


#pour envoyer dans un file kafka une image avec un bioId
def fill_kafka_picture_idbio(json, bio_id, producer, topic):
    #construction du json
    picture_idbio = {
        "idBio": bio_id,
        "picture": json
    }

    producer.send(topic, value=(picture_idbio))

