import json
from factories.traffic_message_factory import TrafficMessageFactory
from factories.traffic_subgroup_message_factory import TrafficSubgroupMessageFactory
from models.traffic_message import TrafficMessage

class AvailableTopicsService:

    def __init__(self, json_file):
        self.json_file = json_file
        self.topics = {}

    def __get_json(self):
        with open(self.json_file) as file:
            data = json.load(file)
            return data


    def get_topics(self) -> dict:
        data: dict = self.__get_json()
        traffic_message_factory = TrafficMessageFactory()
        traffic_subgroup_factory = TrafficSubgroupMessageFactory()

        topics = data.get("topics")
        intersections = data.get("intersections")

        for topic in topics:
            #TODO This is also done in the Message Factory. Duplicate code.
            length = len(topic.get("topic").split("/"))
            if length < 6:
                traffic_message = traffic_message_factory.make_traffic_message(topic.get("topic"), "0")
                self.topics.update({traffic_message.topic: traffic_message})
            else:
                traffic_message = traffic_subgroup_factory.make_traffic_message(topic.get("topic"), "0")
                self.topics.update({traffic_message.topic: traffic_message})

        for intersection in intersections:
            key, value = list(intersection.items())[0]

            intersect_one: TrafficMessage = self.topics.get(key)
            # intersect_two: TrafficMessage = self.topics.get(value)

            intersect_one.intersections.append(value)
            # intersect_two.intersections.append(key)

        return self.topics
