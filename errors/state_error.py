from errors.topic_error import TopicError


class StateError(TopicError):
    def __init__(self, topic, state, expected_state):
        super().__init__(topic)
        self.payload = state
        self.expected_payload = expected_state