import paho.mqtt.client as mqtt
import traffic_topic_feeder
from enum import Enum
from zenlog import log

def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code:" + str(rc))
    client.subscribe("$SYS")
    client.subscribe("8/motorised/north/0/0/traffic_light/0")


def on_message(client, userdata, msg):
    log.info(msg.topic + " " + str(msg.payload))


listener = mqtt.Client()
publisher = mqtt.Client()

listener.on_connect = on_connect
listener.on_message = on_message

feeder = traffic_topic_feeder.TrafficTopicFeeder(publisher)
feeder.add_topic("/test")
feeder.feed_topic()

listener.connect("91.121.165.36", 1883, 60)
publisher.connect("91.121.165.36", 1883, 60)

listener.subscribe("24/motorised/north/0/0/traffic_light/0")

publisher.publish("/test", "Test Message")

publisher.loop_forever()
listener.loop_forever()
