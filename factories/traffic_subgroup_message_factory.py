from factories.traffic_message_factory import TrafficMessageFactory
from models.traffic_subgroup_message import  TrafficSubgroupMessage

class TrafficSubgroupMessageFactory(TrafficMessageFactory):
    def __init__(self):
        super().__init__()
        self.message_order = {
            0: "team_id",
            1: "lane_type",
            2: "group_id",
            3: "subgroup_id",
            4: "component_type",
            5: "component_id"
        }
        self.type = TrafficSubgroupMessage
