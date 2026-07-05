import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from kafka import KafkaProducer
from simulator import TrafficSimulator
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

simulator = TrafficSimulator()

print("🚀 Producer Started...")

while True:
    metrics = simulator.generate_metrics()

    producer.send(
        "traffic-data",
        metrics
    )

    producer.flush()

    print("Sent:", metrics)

    time.sleep(1)