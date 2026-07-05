class BayesianInference:
    """
    Bayesian-based probability estimation for future traffic surge.
    Uses CPU, Memory, Latency and Traffic Spike.
    """

    def __init__(self):
        self.prior = 0.10

    def predict(self, cpu, memory, latency, traffic_spike):

        probability = self.prior

        # CPU Contribution
        if cpu > 90:
            probability += 0.40
        elif cpu > 75:
            probability += 0.30
        elif cpu > 60:
            probability += 0.20
        elif cpu > 40:
            probability += 0.10

        # Memory Contribution
        if memory > 80:
            probability += 0.15
        elif memory > 60:
            probability += 0.10

        # Latency Contribution
        if latency > 80:
            probability += 0.20
        elif latency > 60:
            probability += 0.10

        # Traffic Spike Contribution
        if traffic_spike:
            probability += 0.20

        probability = min(probability, 0.99)

        return round(probability, 2)