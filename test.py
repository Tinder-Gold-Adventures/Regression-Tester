from enum import Enum
from models.traffic_message import TrafficMessage
from factories.TrafficMessageFactory import TrafficMessageFactory
from zenlog import log

class Color(Enum):
    RED = 0
    GREEN = 2
    ORANGE = 1


properties = ["payload", "topic", "team_id", "group_id", "lane_type", "component_type"]

traffic_factory = TrafficMessageFactory()

log.info("Hello test123")

# This should work.
message: TrafficMessage = traffic_factory.make_traffic_message("<24>/<motorised>/<1>/<traffic_light>/<0>", "0")

# This should tell the nr. of properties given is not equal to the expected length.
message2: TrafficMessage = traffic_factory.make_traffic_message("<24>/<motorised>/<1>/<traffic_light>/<0>/<lane>", "1")

#TODO: Implement testing library :)


