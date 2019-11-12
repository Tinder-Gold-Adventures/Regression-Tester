from models.mqtt_message import MQTTMessage

class MQTTSubgroupMessage(MQTTMessage):
    def __init__(self):
        super().__init__()
        self.subgroup_id = str