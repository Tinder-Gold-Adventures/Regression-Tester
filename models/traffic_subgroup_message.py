from models.traffic_message import TrafficMessage

class TrafficSubgroupMessage(TrafficMessage):
    def __init__(self):
        super().__init__()
        self.subgroup = str
