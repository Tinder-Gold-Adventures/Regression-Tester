from sequences.mqtt_sequence import MQTTSeqeunce
from zenlog import log
from models.sequence import Sequence

class TrackSequence(MQTTSeqeunce):

    def __init__(self, topics):
        super().__init__()
        self.topics = topics

    def setup_sequence(self):
        self.sequence_topics.append(Sequence("*/track/0/warning_light/0", "1", self.notify_sequence_start))  # Warning lights on
        self.sequence_topics.append(Sequence("*/track/0/barrier/0", "1", self.check_warning_lights_on)) # Close barriers
        self.sequence_topics.append(Sequence("*/track/0/sensor/1", "1", self.check_train_passing)) # Train passing
        self.sequence_topics.append(Sequence("*/track/0/sensor/1", "0", self.notify_train_passed)) # Train passed
        self.sequence_topics.append(Sequence("*/track/0/barrier/0", "0", self.check_train_passed))  # Close barriers
        self.sequence_topics.append(Sequence("*/track/0/warning_light/0", "0", self.notify_sequence_end))  # Close barriers

    def notify_sequence_end(self):
        log.info("Track sequence ended")

    # TODO: Generalize this method into parent class: Very similar code in vessel_sequence.py
    def notify_sequence_start(self):
        log.info("Track sequence started: Monitoring now.")

    def check_train_passed(self):
        train_light_east = self.topics.get("*/track/0/train_light/0")
        train_light_west = self.topics.get("*/track/0/train_light/1")

        if train_light_east.payload == "0" and train_light_west.payload == "0":
            log.info("Track sequence OK. Train lights are red.")
            return True
        else:
            log.error("Track Sequence ERROR! Payload not matching expected state: Train lights are still green!")
            return False

    def notify_train_passed(self):
        log.info("Track sequence OK. Train passed")

    def check_train_passing(self):
        self.check_warning_lights_on()

        train_light_east = self.topics.get("*/track/0/train_light/0")
        train_light_west = self.topics.get("*/track/0/train_light/1")

        if train_light_east.payload == "0" and train_light_west.payload == "0":
            log.error("Track sequence ERROR! Payload not matching expected state: Both train lights are red!")
            return

        if train_light_east.payload == "1" and train_light_west.payload == "1":
            log.error("Track sequence ERROR! Payload not matching expected state: Both train lights are green!")
            return

        log.info("Track sequence OK. Train light is green")

    # TODO: Generalize this method into parent class: Very similar code in vessel_sequence.py
    def check_warning_lights_on(self):
        warning_light = self.topics.get("*/track/0/warning_light/0")

        if warning_light.payload == "1":
            log.info("Track sequence OK. Warning lights are on.")
            return True
        else:
            log.error("Track Sequence ERROR! Payload not matching expected state: Warning lights are not on!")
            return False
