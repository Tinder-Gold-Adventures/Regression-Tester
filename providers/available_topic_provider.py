import json

from factories.sensor_message_factory import SensorMessageFactory
from factories.traffic_light_message_factory import TrafficLightMessageFactory
from models.traffic_light_message import TrafficLightMessage

class AvailableTopicsService:

    def __init__(self, json_file, team_id):
        self.json_file = json_file
        self.traffic_lights = {}
        self.sensors = {}
        self.data = self.__get_json()
        self.team_id = team_id

    def __get_json(self):
        with open(self.json_file) as file:
            data = json.load(file)
            return data


    def get_traffic_lights(self) -> dict:
        traffic_message_factory = TrafficLightMessageFactory()

        # UPDATE TEAM_ID
        traffic_lights = self.data.get("traffic_lights")
        intersections = self.data.get("intersections")

        for topic in traffic_lights:
            traffic_message = traffic_message_factory.make_message(topic.get("topic"), "0")
            self.traffic_lights.update({traffic_message.topic: traffic_message})

        for intersection in intersections:
            key, value = list(intersection.items())[0]

            intersect: TrafficLightMessage = self.traffic_lights.get(key)
            intersect.intersections.append(value)

        return self.traffic_lights

    def get_sensors(self) -> dict:
        sensor_message_factory = SensorMessageFactory()

        sensors = self.data.get("sensors")
        #UPDATE TEAM_ID
        for topic in sensors:
            sensor_message = sensor_message_factory.make_message(topic.get("topic"), "0")
            self.sensors.update({sensor_message.topic: sensor_message})

        return self.sensors




