from factories.traffic_message_factory import TrafficMessageFactory
from factories.traffic_subgroup_message_factory import TrafficSubgroupMessageFactory
from providers.available_topic_provider import AvailableTopicsService
import paho.mqtt.client as mqtt
from regression_tester import RegressionTester
from handlers.regression_error_handler import RegressionErrorHandler

def on_connect(client, userdata, flags, rc):
    client.subscribe("$SYS")
    client.subscribe("24/#")

def on_message(client, userdata, msg):
    #TODO: Dispose this on a coroutine.
    topic = msg.topic
    payload = str(msg.payload, 'utf-8')
    regression_tester.handle_message(topic, payload)

listener = mqtt.Client()

listener.on_connect = on_connect
listener.on_message = on_message

listener.connect("62.210.180.72", 1883, 60)

listener.subscribe("/24/#")

traffic_factory = TrafficMessageFactory()
traffic_subgroup_factory = TrafficSubgroupMessageFactory()

topic_provider: AvailableTopicsService = AvailableTopicsService("ruleset.json")
topics = topic_provider.get_topics()

error_handler = RegressionErrorHandler()

regression_tester = RegressionTester(topics, error_handler)

listener.loop_forever()




# Checks if incoming messages are valid




# TODO: Implement testing library :)
# TODO: Write unit tests for collisions.
# TODO: Make group number dynamic
# TODO: Refector Available Topic Provider and message factory
# TODO: Make UML
