import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Predator-Prey Ecosystem Lab",
    page_icon="🌿",
    layout="wide"
)

# ---------------- DARK DASHBOARD STYLE ----------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%,
        rgba(0,255,170,0.09), transparent 38%),
        #071019;
    color: #e8f1f7;
}

[data-testid="stSidebar"] {
    background: #0b1722;
    border-right: 1px solid #1d3544;
}

h1, h2, h3 {
    color: #f0f8ff;
}

.metric-card {
    background: linear-gradient(
        145deg, #112531, #091721
    );
    border: 1px solid #244353;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 10px;
    box-shadow: 0 0 15px rgba(0,240,180,0.05);
}

.metric-label {
    color: #8da7b7;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.metric-value {
    color: #52f5bd;
    font-size: 30px;
    font-weight: bold;
    margin-top: 5px;
}

.metric-note {
    color: #8da7b7;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIMULATION MODEL ----------------

def simulate(
    days,
    rabbits_start,
    wolves_start,
    rabbit_growth,
    predation_rate,
    wolf_conversion,
    wolf_death,
    carrying_capacity
):
    """
    Simulates a simplified predator-prey ecosystem.

    Rabbits grow logistically and are eaten by wolves.
    Wolves gain population through predation and lose
    population through natural mortality.
    """

    rabbits = np.zeros(days + 1)
    wolves = np.zeros(days + 1)

    rabbits[0] = rabbits_start
    wolves[0] = wolves_start

    for day in range(days):

        R = rabbits[day]
        W = wolves[day]

        # Rabbit growth slows near carrying capacity.
        prey_growth = (
            rabbit_growth * R *
            (1 - R / carrying_capacity)
        )

        # Predation increases when both populations are large.
        predation = predation_rate * R * W

        # Update rabbit population.
        next_rabbits = R + prey_growth - predation

        # Update wolf population.
        next_wolves = (
            W
            + wolf_conversion * predation
            - wolf_death * W
        )

        # Prevent negative populations.
        rabbits[day + 1] = max(0, next_rabbits)
        wolves[day + 1] = max(0, next_wolves)

    return pd.DataFrame({
        "Day": np.arange(days + 1),
        "Rabbits": rabbits,
        "Wolves": wolves
    })


# ---------------- DASHBOARD HEADER ----------------

st.markdown(
    "<p style='color:#52f5bd; letter-spacing:4px;'>"
    "FIELD RESEARCH / ECOLOGY SIMULATION"
    "</p>",
    unsafe_allow_html=True
)

st.title("🌿 Predator–Prey Ecosystem Lab")

st.markdown("""
Welcome to your virtual ecosystem research lab.

Investigate how rabbit populations, wolf populations,
predation, and environmental limits interact.

Change the experimental conditions in the sidebar
and observe how the ecosystem responds.
""")


# ---------------- SIDEBAR CONTROLS ----------------

with st.sidebar:

    st.header("Experiment Controls")

    days = st.slider(
        "Simulation duration (days)",
        min_value=30,
        max_value=500,
        value=200,
        step=10
    )

    rabbits_start = st.slider(
        "Starting rabbit population",
        min_value=10,
        max_value=500,
        value=120,
        step=10
    )

    wolves_start = st.slider(
        "Starting wolf population",
        min_value=1,
        max_value=100,
        value=18
    )

    st.divider()

    st.subheader("Ecological Parameters")

    rabbit_growth = st.slider(
        "Rabbit growth rate",
        min_value=0.01,
        max_value=0.80,
        value=0.22,
        step=0.01
    )

    predation_rate = st.slider(
        "Predation rate",
        min_value=0.0001,
        max_value=0.0100,
        value=0.0018,
        step=0.0001,
        format="%.4f"
    )

    wolf_conversion = st.slider(
        "Predation-to-wolf conversion",
        min_value=0.01,
        max_value=0.30,
        value=0.08,
        step=0.01
    )

    wolf_death = st.slider(
        "Wolf loss rate",
        min_value=0.01,
        max_value=0.50,
        value=0.12,
        step=0.01
    )

    carrying_capacity = st.slider(
        "Rabbit carrying capacity",
        min_value=100,
        max_value=1500,
        value=600,
        step=25
    )

    st.caption(
        "Carrying capacity represents resource limits, "
        "such as food and available habitat."
    )


# ---------------- RUN THE MODEL ----------------

data = simulate(
    days=days,
    rabbits_start=rabbits_start,
    wolves_start=wolves_start,
    rabbit_growth=rabbit_growth,
    predation_rate=predation_rate,
    wolf_conversion=wolf_conversion,
    wolf_death=wolf_death,
    carrying_capacity=carrying_capacity
)

final_rabbits = data["Rabbits"].iloc[-1]
final_wolves = data["Wolves"].iloc[-1]

peak_rabbits = data["Rabbits"].max()
peak_wolves = data["Wolves"].max()

rabbit_peak_day = int(data["Rabbits"].idxmax())
wolf_peak_day = int(data["Wolves"].idxmax())

rabbit_change = (
    (final_rabbits - rabbits_start)
    / rabbits_start * 100
)

wolf_change = (
    (final_wolves - wolves_start)
    / wolves_start * 100
)


# ---------------- POPULATION SUMMARY ----------------

st.subheader("Population Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Rabbits at End</div>
        <div class="metric-value">
            {final_rabbits:,.1f}
        </div>
        <div class="metric-note">
            {rabbit_change:+.1f}% from start
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Wolves at End</div>
        <div class="metric-value">
            {final_wolves:,.1f}
        </div>
        <div class="metric-note">
            {wolf_change:+.1f}% from start
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Peak Rabbits</div>
        <div class="metric-value">
            {peak_rabbits:,.1f}
        </div>
        <div class="metric-note">
            Day {rabbit_peak_day}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Peak Wolves</div>
        <div class="metric-value">
            {peak_wolves:,.1f}
        </div>
        <div class="metric-note">
            Day {wolf_peak_day}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- POPULATION GRAPH ----------------

st.subheader("Population Dynamics")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data["Day"],
    y=data["Rabbits"],
    name="Rabbits (Prey)",
    mode="lines",
    line=dict(
        color="#52f5bd",
        width=3
    ),
    fill="tozeroy",
    fillcolor="rgba(82,245,189,0.06)",
    hovertemplate=(
        "Day %{x}<br>"
        "Rabbits: %{y:,.1f}"
        "<extra></extra>"
    )
))

fig.add_trace(go.Scatter(
    x=data["Day"],
    y=data["Wolves"],
    name="Wolves (Predators)",
    mode="lines",
    line=dict(
        color="#63b8ff",
        width=3
    ),
    hovertemplate=(
        "Day %{x}<br>"
        "Wolves: %{y:,.1f}"
        "<extra></extra>"
    )
))

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#071019",
    font=dict(color="#c8d6e0"),
    height=450,
    xaxis=dict(
        title="Time (days)",
        gridcolor="rgba(135,170,190,0.12)"
    ),
    yaxis=dict(
        title="Modeled population",
        gridcolor="rgba(135,170,190,0.12)"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ),
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------- PHASE-SPACE GRAPH ----------------

st.subheader("Predator–Prey Relationship")

st.markdown("""
This graph plots wolf population against rabbit population.
It helps reveal how the two populations change together.
""")

phase = go.Figure()

phase.add_trace(go.Scatter(
    x=data["Rabbits"],
    y=data["Wolves"],
    mode="lines",
    line=dict(
        color="#bd8cff",
        width=3
    ),
    name="Population trajectory"
))

phase.add_trace(go.Scatter(
    x=[data["Rabbits"].iloc[0]],
    y=[data["Wolves"].iloc[0]],
    mode="markers",
    marker=dict(
        size=12,
        color="white"
    ),
    name="Starting population"
))

phase.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#071019",
    font=dict(color="#c8d6e0"),
    height=350,
    xaxis=dict(
        title="Rabbit population",
        gridcolor="rgba(135,170,190,0.12)"
    ),
    yaxis=dict(
        title="Wolf population",
        gridcolor="rgba(135,170,190,0.12)"
    )
)

st.plotly_chart(
    phase,
    use_container_width=True
)


# ---------------- EXPERIMENT READOUT ----------------

st.subheader("Research Readout")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Starting rabbits:** {rabbits_start}")
    st.write(f"**Starting wolves:** {wolves_start}")
    st.write(f"**Rabbit peak:** {peak_rabbits:.1f}")
    st.write(f"**Wolf peak:** {peak_wolves:.1f}")

with col2:
    st.write(f"**Final rabbits:** {final_rabbits:.1f}")
    st.write(f"**Final wolves:** {final_wolves:.1f}")
    st.write(f"**Rabbit peak day:** {rabbit_peak_day}")
    st.write(f"**Wolf peak day:** {wolf_peak_day}")

if final_rabbits < 1 and final_wolves < 1:
    st.warning(
        "Both populations are nearly extinct "
        "at the end of this simulation."
    )

elif final_rabbits < 1:
    st.warning(
        "The rabbit population is nearly extinct. "
        "The wolves may also decline without sufficient prey."
    )

elif final_wolves < 1:
    st.info(
        "The wolf population is nearly extinct. "
        "With reduced predation, rabbits may recover."
    )

else:
    st.success(
        "Both populations remain present at the end. "
        "Inspect the graphs to investigate their trends."
    )


# ---------------- BIOLOGY EXPLANATION ----------------

with st.expander("How the Biology Works"):

    st.markdown(r"""
### 1. Rabbit population

The rabbit population follows a logistic-growth model
with an additional predation term.

\[
\Delta R =
rR\left(1-\frac{R}{K}\right)-aRW
\]

- \(R\): rabbit population
- \(W\): wolf population
- \(r\): intrinsic rabbit growth rate
- \(K\): carrying capacity
- \(a\): predation strength

When rabbit numbers are low relative to carrying capacity,
logistic growth can be rapid.

As the population approaches carrying capacity, competition
for limited resources slows population growth.

Wolves also reduce rabbit numbers through predation.

### 2. Wolf population

\[
\Delta W = eaRW-mW
\]

- \(e\): conversion scaling from prey consumption
  to predator population growth
- \(m\): wolf loss rate

In the model, predation can increase the wolf population,
while natural losses reduce it.

### 3. Why the populations affect one another

More rabbits can mean more available food for wolves.

More wolves can mean greater predation pressure on rabbits.

If rabbits become scarce, wolves may eventually decline.
Reduced predation may then allow rabbits to recover.

These feedbacks can produce changing population patterns.
The exact outcome depends on the parameter values.
""")


# ---------------- MODEL LIMITATIONS ----------------

with st.expander("Scientific Assumptions and Limitations"):

    st.markdown("""
- The habitat is treated as one well-mixed environment.
- Rabbits grow logistically; grass is not simulated separately.
- Predation is proportional to the product of rabbit and wolf abundance.
- Animals do not migrate between habitats.
- There are no seasons, diseases, weather events, or random chance.
- Age structure, gestation, hunting success, and territory size
  are not explicitly modeled.
- All parameters remain constant throughout a run.
- The equations are updated in daily steps, using a simple
  Euler-style numerical method.
- Fractional populations are mathematical approximations,
  not literal counts of individual animals.

This is an educational model inspired by Lotka–Volterra
predator–prey equations with logistic prey growth. It is
not calibrated to predict a particular real ecosystem.
""")


# ---------------- DEMONSTRATION EXPERIMENT ----------------

with st.expander("Suggested Classroom Experiment"):

    st.markdown("""
### Research question

What happens when predation pressure increases?

**Step 1:** Run the default simulation.

Record the rabbit peak, wolf peak, and final populations.

**Step 2:** Change only the predation rate from `0.0018`
to `0.0030`.

**Step 3:** Record the new values and compare both graphs.

**Step 4:** Explain how increased predation changes rabbit
survival and how prey availability may affect wolves.

### Hypothesis

If predation pressure increases while other parameters
remain constant, rabbits will experience greater losses
from predation.

The effect on wolves depends on the balance between food
availability and their modeled loss rate.

Use your actual results as evidence. Do not assume that
every parameter change produces the same outcome.
""")


# ---------------- EXPORT DATA ----------------

st.subheader("Export Your Research Data")

csv_data = data.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Population Data (CSV)",
    data=csv_data,
    file_name="predator_prey_results.csv",
    mime="text/csv"
)

st.caption(
    "Educational simulation only. Results are determined "
    "by simplified equations and selected parameters."
)