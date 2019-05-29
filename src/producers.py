
def fill_kafka(json, bio_id, producer, topic):

    producer.send(topic, value=(json, bio_id))
