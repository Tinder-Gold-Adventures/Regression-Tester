from abc import abstractmethod

class MQTTMessage:
    def __init__(self):
        self.topic, self.payload = str, str
        self.intersections = []

        self.schema = {
            'topic': {'type': 'string'},
            'payload': {'type': 'string', 'min': 10},}

    @abstractmethod
    def build_schema(self):
        pass
