from models.traffic_light_message import TrafficLightMessage
from factories.message_factory import MessageFactory
from zenlog import log

from models.traffic_light_subgroup_message import TrafficLightSubgroupMessage

traffic_message_parse_order = {
    0: "team_id",
    1: "lane_type",
    2: "group_id",
    3: "component_type",
    4: "component_id"
}

traffic_subgroup_message_parse_order = {
    0: "team_id",
    1: "lane_type",
    2: "group_id",
    3: "subgroup_id",
    4: "component_type",
    5: "component_id"
}

parse_order = {
    TrafficLightMessage: traffic_message_parse_order,
    TrafficLightSubgroupMessage: traffic_subgroup_message_parse_order
}

class TrafficLightMessageFactory(MessageFactory):
    def __init__(self):
        super().__init__()
        self.parse_order = parse_order
        self.type = TrafficLightMessage

    def determine_type(self, list):
        if len(list) == 5:
            return TrafficLightMessage
        elif len(list) == 6:
            return TrafficLightSubgroupMessage
        else:
            raise ValueError("Number of given arguments not matching needed number "
                             "of arguments for object instantiation.")
