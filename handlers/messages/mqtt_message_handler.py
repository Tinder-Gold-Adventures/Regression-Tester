from errors.invalid_value_error import InvalidValueError
from errors.topic_error import TopicError


class MQTTMessageHandler:
    def __init__(self, accepted_values):
        self.accepted_values = accepted_values

    def handle_message(self, topic, payload):
        self.check_if_valid_value(topic, payload)

    def check_if_valid_value(self, topic, payload):
        if self.accepted_values.get(topic.component_type) is not None:
            if payload in self.accepted_values.get(topic.component_type):
                return True
            else:
                raise InvalidValueError(topic.topic, payload)
        else:
            raise TopicError(topic.topic)
