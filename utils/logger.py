import csv
import os


class CSVLogger:

    def __init__(self):

        self.filename = "data/metrics.csv"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.filename):

            with open(self.filename, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Time",
                    "CPU",
                    "Memory",
                    "Requests",
                    "Latency",
                    "Traffic State",
                    "Traffic Surge Probability",
                    "Decision"
                ])

    def log(self, metrics, state, probability, action):

        with open(self.filename, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                metrics["time"],
                metrics["cpu"],
                metrics["memory"],
                metrics["requests_per_second"],
                metrics["latency"],
                state,
                probability,
                action
            ])