import unittest
from providers.available_topic_provider import AvailableTopicsService

class TestIntersections(unittest.TestCase):

    # Asserts that intersections go both ways.
    def test_intersections_equal(self):
        available_topics_service = AvailableTopicsService("../ruleset.json")
        topics = available_topics_service.get_topics()
        for topic in topics.values():
            for intersection in topic.intersections:
                self.assertIn(topic.topic, topics.get(intersection).intersections)