class MarkovChain:
    """
    Markov Chain Traffic State Predictor.
    """

    def __init__(self):
        self.current_state = "LOW"

    def predict_state(self, cpu):

        previous = self.current_state

        if cpu < 30:
            next_state = "LOW"

        elif cpu < 60:
            next_state = "MEDIUM"

        elif cpu < 85:
            next_state = "HIGH"

        else:
            next_state = "PEAK"

        # Prevent sudden jumps between LOW and PEAK
        if previous == "LOW" and next_state == "PEAK":
            next_state = "HIGH"

        elif previous == "PEAK" and next_state == "LOW":
            next_state = "MEDIUM"

        self.current_state = next_state

        return self.current_state