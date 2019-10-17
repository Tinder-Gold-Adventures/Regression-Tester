from enum import Enum
from models.traffic_subgroup_message import TrafficSubgroupMessage
from factories.traffic_message_factory import TrafficMessageFactory
from factories.traffic_subgroup_message_factory import TrafficSubgroupMessageFactory
from providers.available_topic_provider import AvailableTopicsService
from models.traffic_message import TrafficMessage
import paho.mqtt.client as mqtt
from zenlog import log

class RegressionTester:
    def __init__(self, topics):
        self.topics = topics

    def test_valid_message(self, topic, payload):
        topic_object: TrafficMessage = self.topics.get(topic)
        if payload == '2':
            for intersection in topic_object.intersections:
                intersect_object: TrafficMessage = self.topics.get(intersection)
                if intersect_object.payload != '0':
                    raise AssertionError("Intersecting objects traffic light is not on red")
        return True

    def change_topic(self, topic, payload):
        try:
            self.test_valid_message(topic, payload)
        except AssertionError:
            log.error("Collision detected!")

        self.topics.get(topic).payload = payload
        log.info("New payload set")

    # Sets the new state by payload
    def set_state(self, topic, payload):
        return

def on_connect(client, userdata, flags, rc):
    client.subscribe("$SYS")
    client.subscribe("24/#")


def on_message(client, userdata, msg):
    #TODO: Dispose this on a coroutine.
    topic = msg.topic
    payload = str(msg.payload, 'utf-8')
    regression_tester.change_topic(topic, payload)


listener = mqtt.Client()

listener.on_connect = on_connect
listener.on_message = on_message

listener.connect("91.121.165.36", 1883, 60)

listener.subscribe("/24/#")


traffic_factory = TrafficMessageFactory()
traffic_subgroup_factory = TrafficSubgroupMessageFactory()

topic_provider: AvailableTopicsService = AvailableTopicsService("ruleset.json")
topics = topic_provider.get_topics()

regression_tester = RegressionTester(topics)

listener.loop_forever()




# Checks if incoming messages are valid




# TODO: Implement testing library :)
