from abc import ABC, abstractmethod

class MessageFactory(ABC):
    def __init__(self):
        self.parse_order = {}

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

    @abstractmethod
    def determine_type(self, list):
        pass