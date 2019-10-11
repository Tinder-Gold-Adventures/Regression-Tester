from models.traffic_message import TrafficMessage


class TrafficMessageFactory():
    def __init__(self):
        self.message_order = {
            0: "team_id",
            1: "lane_type",
            2: "group_id",
            3: "component_type",
            4: "component_id"
        }

    # Make traffic message
    def make_traffic_message(self, topic: str, payload: str):
        traffic_message = TrafficMessage()

        property_list = self.__topic_to_list(topic)

        self.__try_parse_traffic_message(property_list, traffic_message)

        traffic_message.payload = payload
        traffic_message.topic = topic

        return traffic_message

    # Check if the expected properties exist in the class trying to parse to
    # TODO: Build in object validation using Python package: Cerberus (Object Validation)
    def __try_parse_traffic_message(self, properties: list, traffic_message: TrafficMessage):
        prop_length = len(properties)
        expected_length = len(self.message_order)

        if prop_length != expected_length:
            # TODO: Implement logging library with different levels of logging.
            print("Number of expected properties for TrafficMessage does not match. Expected: "
                  + str(expected_length) + "; Given: " + str(prop_length) + ";")
            return

        for i in range(len(properties)-1):
            try:
                attr = self.message_order[i]
                getattr(traffic_message, attr)
            except AttributeError:
                class_name = type(traffic_message).__name__
                # TODO: Implement logging library with different levels of logging.
                print("Property unknown. Cannot convert to " + str(class_name))
                return

            setattr(traffic_message, self.message_order[i], properties[i])

        print("Message OK! Returning now.")
    # Convert the topic from string format to list.
    def __topic_to_list(self, topic: str):
        properties = topic.split("/")
        for i in range(len(properties)):
            properties[i] = self.__strip_string(properties[i])

        return properties

    # Remove the surrounding '<' and '>' angle brackets.
    def __strip_string(self, value: str):
        new_value = value[1:(len(value) - 1)]
        return new_value
