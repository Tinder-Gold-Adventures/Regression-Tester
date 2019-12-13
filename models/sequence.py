class Sequence:
    topic, value = str, str
    callback = classmethod

    def __init__(self, topic, value, callback):
        self.topic = topic
        self.value = value
        self.callback = callback

    def execute(self):
        if self.callback is not None:
            self.callback()
