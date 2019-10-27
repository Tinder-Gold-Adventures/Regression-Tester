from errors.topic_error import TopicError


class InvalidValueError(TopicError):
    def __init__(self, topic, value):
        super().__init__(topic)
        self.value = value