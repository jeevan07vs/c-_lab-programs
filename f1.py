import streamlit as st
import pandas as pd

# ==========================================
# F1 MARINA BAY RACE STRATEGY INTELLIGENCE
# ==========================================

st.set_page_config(
    page_title="F1 Race Strategy AI",
    page_icon="🏎️",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background-color: #10131a;
    color: white;
}
[data-testid="stMetric"] {
    background: #202631;
    padding: 15px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #ff4b4b;
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.title("🏎️ F1 RACE STRATEGY INTELLIGENCE")
st.caption("MARINA BAY CIRCUIT • SINGAPORE • STRATEGY CONTROL")

st.divider()


# ---------- SIDEBAR INPUTS ----------
st.sidebar.header("📡 Live Race Telemetry")

lap = st.sidebar.slider("Current Lap", 1, 52, 31)
position = st.sidebar.slider("Driver Position", 1, 20, 3)

tyre_wear = st.sidebar.slider(
    "Tyre Degradation (%)", 0.0, 100.0, 88.5
)

wear_rate = st.sidebar.slider(
    "Additional Wear Per Lap (%)", 0.1, 5.0, 1.2
)

safety_car = st.sidebar.toggle(
    "Safety Car Active", value=True
)

rain_eta = st.sidebar.slider(
    "Rain ETA (laps)", 0, 20, 1
)

wetness = st.sidebar.slider(
    "Track Wetness (%)", 0.0, 100.0, 12.0
)

fuel = st.sidebar.number_input(
    "Fuel Remaining (kg)", min_value=0.0, value=42.5
)

fuel_burn = st.sidebar.number_input(
    "Fuel Consumption (kg/lap)", min_value=0.1, value=1.7
)

gap_ahead = st.sidebar.number_input(
    "Gap Ahead (seconds)", min_value=0.0, value=4.2
)

gap_behind = st.sidebar.number_input(
    "Gap Behind (seconds)", min_value=0.0, value=11.8
)

st.sidebar.subheader("Strategy Assumptions")

green_pit_loss = st.sidebar.number_input(
    "Green Flag Pit Loss (seconds)", value=22.44
)

sc_pit_loss = st.sidebar.number_input(
    "Safety Car Pit Loss (seconds)", value=11.5
)

remaining = 53 - lap
pit_loss = sc_pit_loss if safety_car else green_pit_loss


# ---------- WEATHER MODEL ----------
def predicted_wetness(future_lap):
    if rain_eta == 0 or future_lap >= rain_eta:
        rain_laps = (
            future_lap if rain_eta == 0
            else future_lap - rain_eta + 1
        )
        return min(100.0, max(wetness, 45.0 + 12.0 * rain_laps))

    return wetness


def tyre_penalty(compound, degradation, track_wetness):
    wear_penalty = degradation / 100.0 * 3.5

    if compound == "Slick":
        weather_penalty = max(
            0.0, (track_wetness - 15.0) / 85.0 * 8.0
        )
    else:
        weather_penalty = max(
            0.0, (40.0 - track_wetness) / 40.0 * 1.3
        )
        weather_penalty += max(
            0.0, (track_wetness - 85.0) * 0.1
        )

    return wear_penalty + weather_penalty


# ---------- STRATEGY SIMULATION ----------
def simulate_strategy(strategy):
    total_time_cost = 0.0
    degradation = tyre_wear
    compound = "Slick"
    pit_done = False

    for future_lap in range(1, remaining + 1):

        # Box immediately
        if strategy == "Box Now" and not pit_done:
            total_time_cost += pit_loss
            compound = "Intermediate"
            degradation = 5.0
            pit_done = True

        # Delay one lap, then pit
        if (
            strategy == "Delay One Lap"
            and future_lap == 2
            and not pit_done
        ):
            total_time_cost += green_pit_loss
            compound = "Intermediate"
            degradation = 5.0
            pit_done = True

        track = predicted_wetness(future_lap)

        total_time_cost += tyre_penalty(
            compound, degradation, track
        )

        rate_multiplier = 1.0 if compound == "Slick" else 0.8
        degradation = min(
            100.0, degradation + wear_rate * rate_multiplier
        )

    if strategy == "Stay Out":
        # No pit stop; retain current tyres throughout.
        pass

    return round(total_time_cost, 2)


strategies = {
    "Box Now": simulate_strategy("Box Now"),
    "Delay One Lap": simulate_strategy("Delay One Lap"),
    "Stay Out": simulate_strategy("Stay Out")
}

best_strategy = min(strategies, key=strategies.get)


# ---------- TOP DASHBOARD ----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Position", f"P{position}")
col2.metric("Laps Remaining", remaining)
col3.metric("Tyre Wear", f"{tyre_wear:.1f}%")
col4.metric(
    "Pit Loss",
    f"{pit_loss:.2f}s",
    delta="Safety Car" if safety_car else "Green Flag"
)

st.divider()


# ---------- STRATEGY RECOMMENDATION ----------
st.subheader("🧠 AI Strategy Recommendation")

weather_risk = rain_eta <= 2 or wetness > 15
tyre_risk = tyre_wear >= 75

if wetness >= 85:
    st.warning(
        "Extreme wetness detected. Evaluate full wet tyres "
        "before choosing intermediates."
    )

if fuel < remaining * fuel_burn:
    st.error(
        "Fuel warning: current fuel is below the estimated "
        "remaining race requirement."
    )

if safety_car and (weather_risk or tyre_risk):
    st.success(
        "🚨 BOX NOW: Safety Car window offers reduced pit loss. "
        "Evaluate intermediate tyres before rain intensifies."
    )
elif tyre_wear >= 95:
    st.error(
        "CRITICAL: Tyres are at extreme degradation. "
        "Pit immediately if the selected compound is suitable."
    )
elif weather_risk:
    st.warning(
        "WEATHER ALERT: Monitor the crossover and prepare "
        "for a wet-weather tyre change."
    )
else:
    st.info(
        f"Monitor conditions. The model's lowest-cost strategy "
        f"is {best_strategy}."
    )

st.write("**Strategy selected by lowest modeled time cost:**",
         best_strategy)

st.divider()


# ---------- STRATEGY COMPARISON ----------
st.subheader("📊 Pit Stop Strategy Comparison")

results = pd.DataFrame({
    "Strategy": list(strategies.keys()),
    "Estimated Time Cost (seconds)": list(strategies.values())
}).sort_values("Estimated Time Cost (seconds)")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    results.set_index("Strategy")
)

best_cost = strategies[best_strategy]

other_costs = [
    value for name, value in strategies.items()
    if name != best_strategy
]

st.metric(
    "Modeled Advantage vs Next Best",
    f"{min(other_costs) - best_cost:.2f} seconds"
)

st.caption(
    "These values are illustrative model estimates, not "
    "validated F1 lap-time predictions."
)

st.divider()


# ---------- POSITION RISK ----------
st.subheader("🏁 Track Position Analysis")

col1, col2 = st.columns(2)

with col1:
    st.metric("Gap to Car Ahead", f"{gap_ahead:.1f}s")
    st.metric("Gap to Car Behind", f"{gap_behind:.1f}s")

with col2:
    if pit_loss >= gap_behind:
        st.warning(
            "Pit-stop risk: nominal pit loss is at least the "
            "current gap behind. A position loss is possible."
        )
    else:
        st.success(
            "Nominal pit loss is smaller than the gap behind. "
            "Position retention is possible, not guaranteed."
        )

    st.write(
        "Actual positions depend on rival pit stops, pit timing, "
        "Safety Car bunching and traffic on rejoin."
    )

st.divider()


# ---------- FUEL ANALYSIS ----------
st.subheader("⛽ Fuel Strategy")

fuel_needed = remaining * fuel_burn
fuel_margin = fuel - fuel_needed

f1, f2, f3 = st.columns(3)

f1.metric("Fuel Available", f"{fuel:.1f} kg")
f2.metric("Estimated Fuel Needed", f"{fuel_needed:.1f} kg")
f3.metric("Fuel Margin", f"{fuel_margin:+.1f} kg")

if fuel_margin < 0:
    st.error("Fuel target not met under current consumption assumptions.")
else:
    st.success("Fuel target met under current consumption assumptions.")

st.divider()


# ---------- WEATHER FORECAST ----------
st.subheader("🌧️ Simplified Track Forecast")

forecast = pd.DataFrame({
    "Lap": list(range(lap + 1, min(54, lap + 9))),
})

forecast["Estimated Wetness (%)"] = [
    predicted_wetness(i)
    for i in range(1, len(forecast) + 1)
]

st.line_chart(
    forecast.set_index("Lap")
)

st.caption(
    "Weather progression is a configurable demonstration heuristic, "
    "not a live weather forecast."
)

st.divider()


# ---------- EXPLANATION ----------
with st.expander("ℹ️ How the strategy engine works"):
    st.markdown("""
    **Inputs**
    - Tyre degradation and projected wear
    - Safety Car status and assumed pit-stop loss
    - Rain ETA and track wetness
    - Fuel availability and consumption
    - Gaps to competitors

    **Strategy options**
    - Box Now: pay the current assumed pit loss and switch to inters.
    - Delay One Lap: stay out briefly, then pit.
    - Stay Out: remain on the current slick tyres.

    **Limitations**
    - No real-time F1 telemetry is connected.
    - Competitor pit strategies are not fully simulated.
    - Weather progression and tyre pace are illustrative.
    - Fuel consumption is assumed constant.
    - The model does not simulate the full race or calculate
      exact finishing positions.
    """)

st.caption(
    "F1 Race Strategy Intelligence • Hackathon Prototype"
)