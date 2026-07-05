from simulator import TrafficSimulator
from models.bayesian import BayesianInference
from models.markov import MarkovChain
from services.decision_engine import DecisionEngine
from utils.logger import CSVLogger
import time

simulator = TrafficSimulator()
bayes = BayesianInference()
markov = MarkovChain()
decision = DecisionEngine()
logger = CSVLogger()

while True:

    metrics = simulator.generate_metrics()

    probability = bayes.predict(
        metrics["cpu"],
        metrics["memory"],
        metrics["latency"],
        metrics["traffic_spike"]
    )

    state = markov.predict_state(
        metrics["cpu"]
    )


    action = decision.decide(
        probability,
        state
    )
    logger.log(
    metrics,
    state,
    probability,
    action
)

    print("=" * 60)
    print(metrics)
    print(f"Traffic State            : {state}")
    print(f"Traffic Surge Probability: {probability * 100:.0f}%")
    print(f"Autoscaler Decision      : {action}")

    time.sleep(1)