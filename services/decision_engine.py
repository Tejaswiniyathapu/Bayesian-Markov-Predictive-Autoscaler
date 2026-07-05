class DecisionEngine:
    """
    Decides whether the system should
    Scale Up, Hold, or Scale Down.
    """

    def decide(self, probability, state):

        if probability >= 0.80 or state == "PEAK":
            return "SCALE UP"

        elif probability <= 0.30 and state == "LOW":
            return "SCALE DOWN"

        else:
            return "HOLD"