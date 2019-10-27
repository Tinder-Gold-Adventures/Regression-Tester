from models.mqtt_message import MQTTMessage


class TrafficLightMessage(MQTTMessage):
    def __init__(self):
        super().__init__()
        self.team_id, self.group_id, self.component_id = str, str, str
        self.lane_type, self.component_type = str, str
        self.intersections = []
