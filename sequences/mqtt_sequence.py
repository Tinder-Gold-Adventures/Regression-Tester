from abc import ABC
from zenlog import log

class MQTTSeqeunce(ABC):

    def __init__(self):
        self.state = 0
        self.sequence_topics = []

    def setup_sequence(self):
        raise NotImplementedError()

    def stop(self):
        log.info("Sequence DONE: Resetting now.")
        self.state = 0
        return

    def handle(self):
        sequence = self.sequence_topics[self.state]
        sequence.execute()

        if self.state + 1 == (len(self.sequence_topics)):
            self.stop()
            return

        self.state = self.state + 1

    def get_topic_names(self):
        topic_names = []

        for sequence in self.sequence_topics:
            topic_names.append(sequence.topic)

        return topic_names


