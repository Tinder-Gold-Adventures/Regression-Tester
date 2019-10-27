from models.sensor_message import SensorMessage


class SensorSubgroupMessage(SensorMessage):
    def __init__(self):
        super().__init__()
        self.subgroup_id = str