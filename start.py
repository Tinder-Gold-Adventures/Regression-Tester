from handlers.errors.log_error_handler import LogErrorHandler
from handlers.messages.mqtt_message_handler import MQTTMessageHandler
from models.mqtt_message import MQTTMessage
from models.mqtt_subgroup_message import MQTTSubgroupMessage
from providers.available_topic_provider import AvailableTopicsService
import paho.mqtt.client as mqtt
from regression_tester import RegressionTester

from zenlog import log

TEAM_ID = 24

# Strip team_id from check
def strip_team_id(msg, team_id):
    id = msg.topic.split("/", 1)
    if id[0] == str(TEAM_ID):
        id[0] = "*"
        message = "/".join(id)
        return message


def on_connect(client, userdata, flags, rc):
    client.subscribe("$SYS")


def on_message(client, userdata, msg):
    topic = strip_team_id(msg, TEAM_ID)
    payload = str(msg.payload, 'utf-8')
    regression_tester.handle_message(topic, payload)

# Setup MQTT Client
listener = mqtt.Client()

listener.on_connect = on_connect
listener.on_message = on_message

listener.connect("62.210.180.72", 1883, 60)

listener.subscribe(str(TEAM_ID) + "/#")
log.info("Listening to team: " + str(TEAM_ID))
# End

# Register all known topics
topic_provider: AvailableTopicsService = AvailableTopicsService("ruleset.json", TEAM_ID)

sensors = topic_provider.get_sensors()
barriers = topic_provider.get_barriers()
traffic_lights = topic_provider.get_traffic_lights()
warning_lights = topic_provider.get_warning_lights()

topics = {**traffic_lights, **sensors, **barriers, **warning_lights}
# End

# Register error handlers
log_error_handler = LogErrorHandler()
error_handler_list = [log_error_handler]
# End

# Register message handlers and accepted payloads per MQTTMessage component_type
accepted_values = {
    'traffic_light': ['0', '1', '2', '3'],
    'warning_light': ['0', '1'],
    'barrier': ['0', '1'],
    'sensor': ['0', '1']
}

mqtt_message_handler = MQTTMessageHandler(accepted_values=accepted_values)

message_handlers = {
    MQTTMessage : mqtt_message_handler,
    MQTTSubgroupMessage : mqtt_message_handler,
}
# End

# Register Regression tester & Get going!
regression_tester = RegressionTester(topics=topics, message_handlers=message_handlers, error_handlers=error_handler_list)

listener.loop_forever()

# End




