from models.traffic_light_message import TrafficLightMessage


class TrafficLightSubgroupMessage(TrafficLightMessage):
    def __init__(self):
        super().__init__()
        self.subgroup_id = str
