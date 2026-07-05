import streamlit as st
import pandas as pd
import time
import os
import redis



# ----------------------------------------------------
# Initialize
# ----------------------------------------------------

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

st.set_page_config(
    page_title="Bayesian-Markov Predictive Autoscaler",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Bayesian-Markov Predictive Autoscaler")
st.caption("AI Powered Cloud Autoscaling using Bayesian Inference + Markov Chains")

placeholder = st.empty()

cpu_history = []
request_history = []
latency_history = []

while True:

    metrics = redis_client.hgetall("latest_metrics")

    if not metrics:

        st.warning("Waiting for Kafka Consumer...")
        time.sleep(1)
        continue

    probability = float(metrics["probability"])
    state = metrics["state"]
    action = metrics["decision"]

    

    cpu_history.append(metrics["cpu"])
    request_history.append(metrics["requests"])
    latency_history.append(metrics["latency"])

    cpu_history = cpu_history[-20:]
    request_history = request_history[-20:]
    latency_history = latency_history[-20:]

    with placeholder.container():

        st.subheader("📊 Live System Status")

        c1, c2, c3 = st.columns(3)

        c1.metric("CPU Usage", f"{float(metrics['cpu']):.2f}%")
        c2.metric("Traffic State", state)
        c3.metric("Autoscaler", action)

        if action == "SCALE UP":
            st.error("🚨 High Traffic Detected! Scaling Up Servers")

        elif action == "HOLD":
            st.success("🟢 System Stable")

        else:
            st.info("🔵 Low Traffic - Scaling Down")

        st.divider()

        c4, c5, c6 = st.columns(3)

        c4.metric("Requests/sec", metrics["requests"])
        c5.metric("Latency", f"{float(metrics['latency']):.2f} ms")
        c6.metric("Traffic Surge", f"{probability * 100:.0f}%")

        st.divider()

        st.subheader("📈 CPU Usage History")
        cpu_df = pd.DataFrame(cpu_history, columns=["CPU"])
        cpu_df = cpu_df.astype(float)

        st.line_chart(cpu_df)

        st.subheader("📈 Requests/sec History")
        request_df = pd.DataFrame(request_history, columns=["Requests"])
        request_df = request_df.astype(int)

        st.line_chart(request_df)

        st.subheader("📈 Latency History")
        latency_df = pd.DataFrame(latency_history, columns=["Latency"])
        latency_df = latency_df.astype(float)

        st.line_chart(latency_df) 

    

        st.divider()
                # ============================================
        # SYSTEM ANALYTICS
        # ============================================

        st.subheader("📊 System Analytics")

        if os.path.exists("data/metrics.csv"):

            try:

                df=pd.read_csv("data/metrics.csv",header=None)
                df.columns= ["Time","CPU","Memory","Requests","Latency","Traffic State","Traffic Surge Probability","Decision"]
                numeric_cols = ["CPU","Memory","Requests","Latency","Traffic Surge Probability"]
                for col in numeric_cols:
                    df[col] = pd.to_numeric(df[col], errors='coerce')


                

                

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Average CPU",
                        f"{df['CPU'].mean():.2f}%"
                    )

                    st.metric(
                        "Maximum CPU",
                        f"{df['CPU'].max():.2f}%"
                    )

                    st.metric(
                        "Average Latency",
                        f"{df['Latency'].mean():.2f} ms"
                    )

                with col2:

                    st.metric(
                        "Highest Requests/sec",
                        int(df["Requests"].max())
                    )

                    st.metric(
                        "Total Records",
                        len(df)
                    )

                    st.metric(
                        "Scale Up Events",
                        len(df[df["Decision"] == "SCALE UP"])
                    )

                st.divider()

                # ============================================
                # RECENT EVENTS
                # ============================================

                st.subheader("📋 Recent Events")

                st.dataframe(
                    df.tail(10),
                    use_container_width=True,
                    hide_index=True
                )

            except Exception as e:

                st.error(f"Analytics Error: {e}")

        else:

            st.warning("metrics.csv not found. Run app.py first.")

        st.divider()

        st.caption(
            f"🕒 Last Updated : {metrics['time']}"
        )

    time.sleep(1)
