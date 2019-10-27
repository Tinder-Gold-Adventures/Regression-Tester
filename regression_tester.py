from zenlog import log
from errors.collision_error import CollisionError
from errors.topic_error import TopicError
from errors.state_error import StateError
from typing import List
from handlers.errors.regression_error_handler import RegressionErrorHandler
from errors.invalid_value_error import InvalidValueError

# TODO: Build Error Handling options.
# TODO: Write this to a logfile in reproducible format

class RegressionTester:
    def __init__(self, topics, message_handlers: dict, error_handlers: List[RegressionErrorHandler]):
        self.topics = topics
        self.error_handlers = error_handlers
        self.message_handlers = message_handlers

    def handle_message(self, topic, payload):
        log.info("Trying to handle message on topic: " + str(topic) + " with payload: " + str(payload))
        topic = self.topics.get(topic)
        if topic is None:
            self.handle_error(TopicError(topic))
        topic_type = type(topic)

        handler = self.message_handlers.get(topic_type)
        try:
            handler.handle_message(self.topics, topic, payload)
        except Exception as err:
            self.handle_error(err)

        topic.payload = payload
        log.info("Message handled. Payload of topic: " + str(topic.topic) + " set to: " + str(payload))

    def handle_error(self, error):
        for handler in self.error_handlers:
            if isinstance(error, CollisionError):
                handler.handle_collision_error(error)
            elif isinstance(error, StateError):
                handler.handle_state_error(error)
            elif isinstance(error, InvalidValueError):
                handler.handle_invalid_value_error(error)
            elif isinstance(error, TopicError):
                handler.handle_topic_error(error)
            else:
                raise error
