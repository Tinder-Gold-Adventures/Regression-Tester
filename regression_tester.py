from zenlog import log
from errors.topic_error import TopicError
from typing import List
from handlers.errors.regression_error_handler import RegressionErrorHandler
from errors.invalid_value_error import InvalidValueError

class RegressionTester:
    def __init__(self, topics, message_handlers: dict, error_handlers: List[RegressionErrorHandler]):
        self.topics = topics
        self.error_handlers = error_handlers
        self.message_handlers = message_handlers

    def handle_message(self, topic, payload):
        log.info("Trying to handle message on topic: " + str(topic) + " with payload: " + str(payload))

        if self.topics.get(topic) is None:
            self.handle_error(TopicError(topic))
            return
        else:
            topic = self.topics.get(topic)

        topic_type = type(topic)

        handler = self.message_handlers.get(topic_type)
        try:
            handler.handle_message(topic, payload)
        except Exception as err:
            self.handle_error(err)

        topic.payload = payload
        log.debug("Message on topic " + str(topic.topic) + " handled.")

    def handle_error(self, error):
        for handler in self.error_handlers:
            if isinstance(error, InvalidValueError):
                handler.handle_invalid_value_error(error)
            elif isinstance(error, TopicError):
                handler.handle_topic_error(error)
            else:
                raise error
