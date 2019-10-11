from models.mqtt_message import MQTTMessage
import cerberus.validator


class TrafficMessage(MQTTMessage):
    def __init__(self):
        super().__init__()
        self.team_id, self.group_id, self.component_id = int, int, int
        self.lane_type, self.component_type = str, str