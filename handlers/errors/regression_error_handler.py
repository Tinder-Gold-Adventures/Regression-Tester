from errors.invalid_value_error import InvalidValueError
from errors.topic_error import TopicError
from abc import abstractmethod

class RegressionErrorHandler:
    @abstractmethod
    def handle_topic_error(self, error: TopicError):
        raise NotImplementedError()

    @abstractmethod
    def handle_invalid_value_error(self, error: InvalidValueError):
        raise NotImplementedError()