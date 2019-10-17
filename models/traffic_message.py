from models.mqtt_message import MQTTMessage
import cerberus.validator


class TrafficMessage(MQTTMessage):
    def __init__(self):
        super().__init__()
        self.team_id, self.group_id, self.component_id = int, int, int
        self.lane_type, self.component_type = str, str

        self.constraints = {
            'team_id': {'type': 'integer', 'min': 1, 'max': 24},
            'group_id': {'type': 'integer', 'min': 0, 'max': 8},
            'component_id': {'type': 'integer'},
            'lane_type': {'type': 'string', 'allowed': ['foot', 'cycle', 'motorised', 'vessel', 'track']},
            'component_type': {'type': 'string', 'allowed': ['traffic_light', 'warning_light', 'sensor', 'barrier']}
        }

        self.build_schema()

    def build_schema(self):
        self.schema.update(self.constraints)
