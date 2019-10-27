from enum import Enum
from errors.invalid_value_error import InvalidValueError
from handlers.messages.mqtt_message_handler import MQTTMessageHandler


class Sensors(Enum):
    LOW = '0'
    HIGH = '1'


class SensorMessageHandler(MQTTMessageHandler):
    def handle_message(self, topics, topic, payload):
        self.check_if_valid_value(topic, payload)

    def check_if_valid_value(self, topic, payload):
        if payload != Sensors.LOW.value and payload != Sensors.HIGH.value:
                raise InvalidValueError(topic, payload)
        return True
