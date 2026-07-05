import sys
from pathlib import Path
import json
import redis

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from kafka import KafkaConsumer
from models.bayesian import BayesianInference
from models.markov import MarkovChain
from services.decision_engine import DecisionEngine

# -------------------------------
# Kafka Consumer
# -------------------------------

consumer = KafkaConsumer(
    "traffic-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# -------------------------------
# AI Models
# -------------------------------

bayes = BayesianInference()
markov = MarkovChain()
decision = DecisionEngine()

# -------------------------------
# Redis Connection
# -------------------------------

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

print("🚀 Consumer Started...")

# -------------------------------
# Consume Messages
# -------------------------------

for message in consumer:

    metrics = message.value

    # Bayesian Prediction
    probability = bayes.predict(
        metrics["cpu"],
        metrics["memory"],
        metrics["latency"],
        metrics["traffic_spike"]
    )

    # Markov Prediction
    state = markov.predict_state(
        metrics["cpu"]
    )

    # Decision Engine
    action = decision.decide(
        probability,
        state
    )

    # Store latest metrics in Redis
    redis_client.hset(
        "latest_metrics",
        mapping={
            "time": metrics["time"],
            "cpu": metrics["cpu"],
            "memory": metrics["memory"],
            "requests": metrics["requests_per_second"],
            "latency": metrics["latency"],
            "traffic_spike": str(metrics["traffic_spike"],),
            "state": state,
            "probability": probability,
            "decision": action
        }
    )

    # Display Output
    print("=" * 60)
    print(metrics)
    print("Traffic State :", state)
    print("Probability   :", probability)
    print("Decision      :", action)
    print("✅ Stored in Redis")