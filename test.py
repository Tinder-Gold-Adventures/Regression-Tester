from factories.traffic_light_message_factory import TrafficLightMessageFactory
from handlers.errors.log_error_handler import LogErrorHandler
from handlers.messages.sensor_message_handler import SensorMessageHandler
from handlers.messages.traffic_light_message_handler import TrafficLightMessageHandler
from models.sensor_message import SensorMessage
from models.sensor_subgroup_message import SensorSubgroupMessage
from models.traffic_light_message import TrafficLightMessage
from models.traffic_light_subgroup_message import TrafficLightSubgroupMessage
from providers.available_topic_provider import AvailableTopicsService
import paho.mqtt.client as mqtt
from regression_tester import RegressionTester
from handlers.errors.mqtt_error_handler import MQTTErrorHandler
from zenlog import log

TEAM_ID = 24

def strip_team_id(msg, team_id):
    id = msg.topic.split("/", 1)
    if id[0] == str(TEAM_ID):
        id[0] = "*"
        message = "/".join(id)
        return message


def on_connect(client, userdata, flags, rc):
    client.subscribe("$SYS")


def on_message(client, userdata, msg):
    #TODO: Dispose this on a coroutine.
    topic = strip_team_id(msg, TEAM_ID)
    payload = str(msg.payload, 'utf-8')
    regression_tester.handle_message(topic, payload)

listener = mqtt.Client()

listener.on_connect = on_connect
listener.on_message = on_message

listener.connect("62.210.180.72", 1883, 60)

listener.subscribe(str(TEAM_ID) + "/motorised/#")
log.info("Listening to team: " + str(TEAM_ID))

traffic_factory = TrafficLightMessageFactory()

topic_provider: AvailableTopicsService = AvailableTopicsService("ruleset.json", TEAM_ID)

traffic_lights = topic_provider.get_traffic_lights()
sensors = topic_provider.get_sensors()

topics = {**traffic_lights, **sensors}

mqtt_error_handler = MQTTErrorHandler(listener)
log_error_handler = LogErrorHandler()
error_handler_list = [mqtt_error_handler, log_error_handler]

traffic_light_message_handler = TrafficLightMessageHandler()
sensor_message_handler = SensorMessageHandler()

message_handlers = {
    TrafficLightMessage : traffic_light_message_handler,
    TrafficLightSubgroupMessage : traffic_light_message_handler,
    SensorMessage : sensor_message_handler,
    SensorSubgroupMessage : sensor_message_handler
}

regression_tester = RegressionTester(topics=topics, message_handlers=message_handlers, error_handlers=error_handler_list)

listener.loop_forever()

# Checks if incoming messages are valid

# TODO: Implement testing library :)
# TODO: Write unit tests for collisions.
# TODO: Make group number dynamic
# TODO: Refector Available Topic Provider and message factory
# TODO: Make UML
