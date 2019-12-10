from abc import ABC
from zenlog import log
from models.sequence import Sequence

class MQTTSeqeunce(ABC):

    def __init__(self):
        self.start_condition, self.stop_condition = dict, dict
        self.started = False
        self.state = 0
        self.sequence_topics = []

    def setup_sequence(self):
        pass

    def stop(self):
        log.info("Sequence done")
        return

    def handle(self, topic, name):
        sequence = self.sequence_topics[self.state]
        sequence.execute()

        if self.state + 1 > (len(self.sequence_topics) + 1):
            self.stop()
            return

        self.state = self.state + 1

    def get_topic_names(self):
        topic_names = []

        for sequence in self.sequence_topics:
            topic_names.append(sequence.topic)

        return topic_names

    def set_start_condition(self, start_condition):
        self.start_condition = start_condition

    def set_stop_condition(self, stop_condition):
        self.stop_condition = stop_condition

