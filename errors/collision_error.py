class CollisionError(Exception):
    def __init__(self, topic, intersection_topic):
        self.topic = topic
        self.intersection_topic = intersection_topic