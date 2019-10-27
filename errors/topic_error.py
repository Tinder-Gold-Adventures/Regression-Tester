class TopicError(Exception):
    def __init__(self, topic):
        #TODO: Make different error for invalid Topic error. (Not existing topic)
        self.topic = topic