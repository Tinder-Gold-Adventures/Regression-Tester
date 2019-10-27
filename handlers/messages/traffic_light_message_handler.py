from enum import Enum

from errors.collision_error import CollisionError
from errors.state_error import StateError
from handlers.messages.mqtt_message_handler import MQTTMessageHandler
from models.traffic_light_message import TrafficLightMessage


class TrafficLights(Enum):
    RED = '0'
    GREEN = '2'
    ORANGE = '1'


def check_if_collision(topics, topic, payload):
    if payload == TrafficLights.GREEN.value:
        for intersection in topic.intersections:
            intersect_object: TrafficLightMessage = topics.get(intersection)
            if intersect_object.payload != TrafficLights.RED.value:
                raise CollisionError(topic.topic, intersect_object.topic)
    return True


def check_next_state_as_expected(topic, payload):
    current_state = topic.payload

    if current_state == TrafficLights.GREEN.value:
        expected_state = TrafficLights.ORANGE.value
    elif current_state == TrafficLights.ORANGE.value:
        expected_state = TrafficLights.RED.value
    else:
        expected_state = TrafficLights.GREEN.value

    if expected_state != payload:
        raise StateError(topic.topic, current_state, expected_state)

    return True


class TrafficLightMessageHandler(MQTTMessageHandler):
    def handle_message(self, topics, topic, payload):
        check_next_state_as_expected(topic, payload)
        check_if_collision(topics, topic, payload)