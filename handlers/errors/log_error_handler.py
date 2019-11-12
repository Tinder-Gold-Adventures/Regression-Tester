from errors.invalid_value_error import InvalidValueError
from handlers.errors.regression_error_handler import RegressionErrorHandler
from errors.topic_error import TopicError
from zenlog import log

class LogErrorHandler(RegressionErrorHandler):

    def handle_topic_error(self, error: TopicError):
        error_message = "Topic: " + str(error.topic) + " is invalid."
        log.error(error_message)

    def handle_invalid_value_error(self, error: InvalidValueError):
        error_message = "Value: " + str(error.value) + " invalid for topic: " + str(error.topic)
        log.error(error_message)
