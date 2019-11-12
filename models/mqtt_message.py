class MQTTMessage:
    def __init__(self):
        self.topic, self.payload = str, str
        self.team_id, self.group_id, self.component_id = str, str, str
        self.lane_type, self.component_type = str, str

