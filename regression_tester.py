from zenlog import log
from models.traffic_message import TrafficMessage
from enum import Enum
from errors.collision_error import CollisionError
from errors.topic_error import TopicError
from errors.state_error import StateError
from handlers.regression_error_handler import RegressionErrorHandler

# TODO: Build Error Handling options.
# TODO: Write this to a logfile in reproducible format

class TrafficLights(Enum):
    RED = '0'
    GREEN = '2'
    ORANGE = '1'

class RegressionTester:
    def __init__(self, topics, error_handler):
        self.topics = topics
        self.error_handler: RegressionErrorHandler = error_handler

    def handle_message(self, topic, payload):
        try:
            self.__check_if_topic_exists(topic)
            self.__check_next_state_as_expected(topic, payload)
            self.__check_if_collision(topic, payload)
        except StateError as err:
            log.error("States not matching")
            self.error_handler.handle_state_error(err)
        except TopicError as err:
            self.error_handler.handle_topic_error(err)
        except CollisionError as err:
            self.error_handler.handle_collision_error(err)

        self.__set_state(topic, payload)
        log.info("New payload set")

    # Returns true if a possible collision is detected.
    def __check_if_collision(self, topic, payload) -> bool:
        topic_object: TrafficMessage = self.topics.get(topic)
        if payload == TrafficLights.GREEN:
            for intersection in topic_object.intersections:
                intersect_object: TrafficMessage = self.topics.get(intersection)
                if intersect_object.payload != TrafficLights.RED:
                    raise CollisionError(topic, intersect_object.topic)
        return True

    # Check if the topic is known within the regression tester
    def __check_if_topic_exists(self, topic):
        exist = self.topics.get(topic)
        if exist is None:
            raise TopicError(topic)
        return True

    # Checks if the next state follows the correct traffic light order (Green, Orange, Red.)
    def __check_next_state_as_expected(self, topic, payload) -> bool:
        current_state = self.topics.get(topic).payload

        if current_state == TrafficLights.GREEN:
            expected_state = TrafficLights.ORANGE
        elif current_state == TrafficLights.ORANGE:
            expected_state = TrafficLights.RED
        else:
            expected_state = TrafficLights.GREEN

        if expected_state != payload:
            raise StateError(current_state, expected_state)

        return True

    # Sets the new state by payload
    def __set_state(self, topic, payload):
        self.topics.get(topic).payload = payload
