from errors.topic_error import TopicError


class CollisionError(TopicError):
    def __init__(self, topic, intersection_topic):
        super().__init__(topic)
        self.intersection_topic = intersection_topic