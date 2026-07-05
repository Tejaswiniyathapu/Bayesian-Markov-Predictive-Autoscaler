import random
import time
from datetime import datetime


class TrafficSimulator:
    """
    Simulates realistic cloud traffic patterns.
    """

    def __init__(self):
        self.current_requests = 200

    def generate_metrics(self):

        hour = datetime.now().hour

        # -----------------------------------
        # Daily traffic pattern
        # -----------------------------------

        if 0 <= hour < 6:
            base_requests = random.randint(100, 300)

        elif 6 <= hour < 10:
            base_requests = random.randint(400, 900)

        elif 10 <= hour < 17:
            base_requests = random.randint(900, 1800)

        elif 17 <= hour < 22:
            base_requests = random.randint(1800, 3200)

        else:
            base_requests = random.randint(300, 800)

        # -----------------------------------
        # Random flash traffic
        # -----------------------------------

        if random.random() < 0.08:
            base_requests += random.randint(500, 1500)

        # -----------------------------------
        # Small natural fluctuations
        # -----------------------------------

        self.current_requests = base_requests + random.randint(-80, 80)

        # -----------------------------------
        # CPU Usage
        # -----------------------------------

        cpu_usage = min(
            100,
            round(
                self.current_requests * 0.03 +
                random.uniform(0, 8),
                2
            )
        )

        # -----------------------------------
        # Memory Usage
        # -----------------------------------

        memory_usage = min(
            100,
            round(
                self.current_requests * 0.02 +
                random.uniform(15, 30),
                2
            )
        )

        # -----------------------------------
        # Latency
        # -----------------------------------

        latency = round(
            15 + cpu_usage * 0.6 + random.uniform(0, 10),
            2
        )

        # -----------------------------------
        # Traffic Spike
        # -----------------------------------

        traffic_spike = self.current_requests > 2500

        return {

            "time": datetime.now().strftime("%H:%M:%S"),

            "requests_per_second": self.current_requests,

            "cpu": cpu_usage,

            "memory": memory_usage,

            "latency": latency,

            "traffic_spike": traffic_spike
        }


if __name__ == "__main__":

    simulator = TrafficSimulator()

    while True:

        print(simulator.generate_metrics())

        time.sleep(1)