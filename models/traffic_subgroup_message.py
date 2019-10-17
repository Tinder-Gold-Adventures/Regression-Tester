from models.traffic_message import TrafficMessage

class TrafficSubgroupMessage(TrafficMessage):
    def __init__(self):
        super().__init__()
        self.subgroup_id = str

        self.build_schema()

    def build_schema(self):
        self.schema.update({
            'subgroup': {'type': 'string'}
        })
