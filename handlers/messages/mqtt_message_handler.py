from abc import abstractmethod

class MQTTMessageHandler():
    @abstractmethod
    def handle_message(self, topics, topic, payload):
        pass
