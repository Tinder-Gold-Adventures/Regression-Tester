from sequences.mqtt_sequence import MQTTSeqeunce
from models.sequence import  Sequence
from zenlog import log

class VesselSequence(MQTTSeqeunce):

    def __init__(self, topics):
        super().__init__()
        self.topics = topics

    def setup_sequence(self):
        self.sequence_topics.append(Sequence("*/vessel/0/warning_light/0", "1", self.notify_sequence_start)) # Warning lights on
        self.sequence_topics.append(Sequence("*/vessel/0/barrier/0", "1", self.check_warning_lights_on)) # Close barriers
        self.sequence_topics.append(Sequence("*/vessel/0/deck/0", "1", self.check_bridge_opening)) # Open the bridge
        self.sequence_topics.append(Sequence("*/vessel/0/deck/0", "0", self.check_bridge_closing)) # Close the brdige

    def notify_sequence_start(self):
        log.info("Bridge sequence started: Monitoring now.")

    def check_bridge_closing(self):
        self.check_warning_lights_on()

        boat_light_east = self.topics.get("*/vessel/0/boat_light/0")
        boat_light_west = self.topics.get("*/vessel/0/boat_light/1")
        bridge_sensor = self.topics.get("*/vessel/0/sensor/3")

        if boat_light_east.payload != "0" or boat_light_west.payload != "0":
            log.error("Bridge sequence ERROR! Payload not matching expected state: The boat lights are not on red!")
        if bridge_sensor.payload != "0":
            log.error("Bridge sequence ERROR! Payload not matching expected state: Sensor values say the bridge "
                      "isn't empty!")

    def check_bridge_opening(self):
        self.check_warning_lights_on()

    def check_warning_lights_on(self):
        warning_light = self.topics.get("*/vessel/0/warning_light/0")

        if warning_light.payload == "1":
            log.info("Bridge sequence OK. Warning lights are on.")
            return True
        else:
            log.error("Bridge sequence ERROR! Payload not matching expected state: Warning lights are not on!")
            return False


