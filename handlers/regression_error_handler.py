from errors.collision_error import CollisionError
from errors.topic_error import TopicError
from errors.state_error import StateError
from zenlog import log
from abc import abstractmethod

class RegressionErrorHandler:
    @abstractmethod
    def handle_state_error(self, error: StateError):
        raise NotImplementedError()

    @abstractmethod
    def handle_collision_error(self, error: CollisionError):
        raise NotImplementedError()

    @abstractmethod
    def handle_topic_error(self, error: TopicError):
        raise NotImplementedError()