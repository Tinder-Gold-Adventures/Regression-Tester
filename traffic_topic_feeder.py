import time, threading
import random
from enum import Enum


class TrafficLights(Enum):
    RED = 0
    GREEN = 2
    ORANGE = 1


class TrafficTopicFeeder:
    def __init__(self, client):
        self.topics = []
        self.values = []
        self.client = client
        self.min_interval = 10
        self.max_interval = 25
        self.enum_index = TrafficLights.RED
        print("Enum index = " + str(self.enum_index))

    # Set min Interval in ms.
    def set_min_interval(self, interval):
        self.min_interval = interval

    # Set max Interval in ms.
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

    def set_next_value(self):
        if self.enum_index == TrafficLights.RED:
            self.enum_index = TrafficLights.GREEN
            return
        if self.enum_index == TrafficLights.GREEN:
            self.enum_index = TrafficLights.ORANGE
            return
        else:
            self.enum_index = TrafficLights.RED

    def feed_topic(self):
        for topic in self.topics:
            print("Writing to topic: " + str(topic) + " with value: " + str(self.enum_index.value))
            self.client.publish(topic, self.enum_index.value)

        next_exec = self.determine_interval()
        threading.Timer(next_exec, self.feed_topic).start()
        self.set_next_value()
        print("Setting traffic light to " + str(self.enum_index) + " in " + str(next_exec) + " seconds")
