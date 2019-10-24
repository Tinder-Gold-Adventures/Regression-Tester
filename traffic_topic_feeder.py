import threading
import random
import json
import paho.mqtt.client as mqtt
from enum import Enum
from zenlog import log


class TrafficLights(Enum):
    RED = 0
    GREEN = 2
    ORANGE = 1


class TrafficTopicFeeder:
    def __init__(self, client):
        self.topics = []
        self.values = []
        self.client = client
        self.min_interval = 3
        self.max_interval = 6
        self.enum_index = TrafficLights.RED

    def set_min_interval(self, interval):
        self.min_interval = interval

    def set_max_interval(self, interval):
        self.max_interval = interval

    def add_value(self, value):
        self.values.append(value)

    def add_topic(self, topic):
        self.topics.append(topic)

    def determine_interval(self):
        if self.enum_index == TrafficLights.ORANGE:
            return 3  # Orange light for about 3 sec.

        return random.randint(self.min_interval, self.max_interval)

    # Sets the next value according to traffic light order
    def set_next_value(self):
        if self.enum_index == TrafficLights.RED:
            self.enum_index = TrafficLights.GREEN
            return
        if self.enum_index == TrafficLights.GREEN:
            self.enum_index = TrafficLights.ORANGE
            return
        else:
            self.enum_index = TrafficLights.RED

    # Publish on topic and enqueues next execution using Threading.Timer
    def feed_topic(self):
        for topic in self.topics:
            log.info("Writing to topic: " + str(topic) + " with value: " + str(self.enum_index.value))
            self.client.publish(topic, self.enum_index.value)

        next_exec = self.determine_interval()
        threading.Timer(next_exec, self.feed_topic).start()
        self.set_next_value()

        log.info("Setting traffic light to " + str(self.enum_index) + " in " + str(next_exec) + " seconds")


def get_json():
    with open("ruleset.json") as file:
        data = json.load(file)
        return data


def on_connect(client, userdata, flags, rc):
    log.info("Connected to client with status code: " + str(rc))


client = mqtt.Client()
client.connect("62.210.180.72", 1883, 60)

client.on_connect = on_connect

topic_feeder = TrafficTopicFeeder(client)

data: dict = get_json()
topics = data.get("topics")

for topic in topics:
    to_feed = topic.get("topic")
    topic_feeder.add_topic(to_feed)

topic_feeder.feed_topic()
