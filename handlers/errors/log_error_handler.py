from errors.invalid_value_error import InvalidValueError
from handlers.errors.regression_error_handler import RegressionErrorHandler
from errors.state_error import StateError
from errors.topic_error import TopicError
from errors.collision_error import CollisionError
from zenlog import log

class LogErrorHandler(RegressionErrorHandler):

    def handle_collision_error(self, error: CollisionError):
        error_message = "Topic: " + str(error.topic) + " intersects with topic: " + error.intersection_topic
        log.error(error_message)

    def handle_state_error(self, error: StateError):
        error_message = "Expected value was: " + str(error.expected_payload) + "; Given value was: " + error.payload + (
                        " for Topic " + str(error.topic))

        log.error(error_message)

    def handle_topic_error(self, error: TopicError):
        error_message = "Topic: " + str(error.topic) + " does not exist."
        log.error(error_message)

    def handle_invalid_value_error(self, error: InvalidValueError):
        error_message = "Value: " + str(error.value) + " invalid for topic: " + str(error.topic)
        log.error(error_message)
