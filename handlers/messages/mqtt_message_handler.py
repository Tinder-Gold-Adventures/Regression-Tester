from abc import abstractmethod

from errors.topic_error import TopicError

class MQTTMessageHandler():
    @abstractmethod
    def handle_message(self, topics, topic, payload):
        pass
