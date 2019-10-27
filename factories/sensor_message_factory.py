from factories.message_factory import MessageFactory
from models.sensor_message import SensorMessage
from models.sensor_subgroup_message import SensorSubgroupMessage

sensor_message_parse_order = {
    0: "team_id",
    1: "lane_type",
    2: "group_id",
    3: "component_type",
    4: "component_id"
}

sensor_subgroup_parse_order = {
    0: "team_id",
    1: "lane_type",
    2: "group_id",
    3: "subgroup_id",
    4: "component_type",
    5: "component_id"
}

parse_order = {
    SensorMessage: sensor_message_parse_order,
    SensorSubgroupMessage: sensor_subgroup_parse_order
}

class SensorMessageFactory(MessageFactory):

    def __init__(self):
        super().__init__()
        self.parse_order = parse_order


    def determine_type(self, list):
        if len(list) == 5:
            return SensorMessage
        elif len(list) == 6:
            return SensorSubgroupMessage
        else:
            raise ValueError("Number of given arguments not matching needed number "
                             "of arguments for object instantiation.")
