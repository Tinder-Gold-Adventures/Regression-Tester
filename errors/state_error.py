class StateError(Exception):
    def __init__(self, state, expected_state):
        self.payload = state
        self.expected_payload = expected_state