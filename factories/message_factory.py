from abc import ABC, abstractmethod

from models.mqtt_message import MQTTMessage
from models.mqtt_subgroup_message import MQTTSubgroupMessage

mqtt_message_parse_order = {
    0: "team_id",
    1: "lane_type",
    2: "group_id",
    3: "component_type",
    4: "component_id"
}

mqtt_subgroup_message_parse_order = {
    0: "team_id",
    1: "lane_type",
    2: "group_id",
    3: "subgroup_id",
    4: "component_type",
    5: "component_id"
}

parse_order = {
    MQTTMessage: mqtt_message_parse_order,
    MQTTSubgroupMessage: mqtt_subgroup_message_parse_order
}

class MessageFactory(ABC):
    def __init__(self):
        self.parse_order = parse_order

    def make_message(self, topic, payload):
        property_list = self.topic_to_list(topic)
        self.type = self.determine_type(property_list)

        try:
            message = self.__parse_message(property_list)
            message.payload = payload
            message.topic = topic
            return message
        except ValueError:
            return
        except AttributeError:
            return

    def __parse_message(self, properties: list):
        message = self.type()

        prop_length = len(properties)
        expected_length = len(self.parse_order.get(self.type))

        if prop_length != expected_length:
            raise ValueError("Given length for " + str(self.type) + " not matching expected length.")

        for i in range(len(properties) - 1):
            attr = self.parse_order.get(self.type)[i]
            getattr(message, attr)
            setattr(message, self.parse_order.get(self.type)[i], properties[i])

        return message

    def topic_to_list(self, topic: str):
        properties = topic.split("/")

        return properties

    def __strip_string(self, value: str):
        new_value = value[1:(len(value) - 1)]
        return new_value

    def determine_type(self, list):
        if len(list) == 5:
            return MQTTMessage
        elif len(list) == 6:
            return MQTTSubgroupMessage
        else:
            raise ValueError("Number of given arguments not matching needed number "
                             "of arguments for object instantiation.")