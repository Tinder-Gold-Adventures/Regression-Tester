import paho.mqtt.client as mqtt
from zenlog import log

def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code:" + str(rc))

def on_message(client, userdata, msg):
    log.info(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.subscribe("24/motorised/north/0/0/traffic_light/0")

