import json

from factories.message_factory import MessageFactory


class AvailableTopicsService:

    def __init__(self, json_file, team_id):
        self.json_file = json_file
        self.data = self.__get_json()
        self.team_id = team_id
        self.message_factory = MessageFactory()

    def __get_json(self):
        with open(self.json_file) as file:
            data = json.load(file)
            return data

    def __get_by_lane_type(self, lane_type):
        rules = self.data.get(lane_type)
        topics = {}

        for topic in rules:
            message = self.message_factory.make_message(topic.get("topic"), "0")
            topics.update({message.topic: message})

        return topics

    def get_warning_lights(self) -> dict:
        return self.__get_by_lane_type("warning_lights")

    def get_barriers(self) -> dict:
        return self.__get_by_lane_type("barriers")

    def get_traffic_lights(self) -> dict:
        return self.__get_by_lane_type("traffic_lights")

    def get_sensors(self) -> dict:
        return self.__get_by_lane_type("sensors")






