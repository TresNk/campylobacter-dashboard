import streamlit as st
import numpy as np
import pandas as pd
from model_simulator import ModelSimulator

st.set_page_config(layout="wide")

st.title('Campylobacteriosis Model Dashboard')
st.write("An interactive dashboard to simulate and visualize the Campylobacteriosis mathematical model.")

# --- Sidebar for Parameters ---
st.sidebar.header('Model Parameters')

params = {}

# Using the same parameter definitions as the Flask app for consistency
param_definitions = {
    'Lambda': {'min_value': 1.0, 'max_value': 100.0, 'value': 50.0, 'step': 1.0, 'name': 'Recruitment Rate (Λ)'},
    'd': {'min_value': 0.00001, 'max_value': 0.0001, 'value': 0.000042, 'step': 0.000001, 'name': 'Natural Death Rate (d)', 'format': '%.6f'},
    'epsilon': {'min_value': 0.0001, 'max_value': 0.001, 'value': 0.00058, 'step': 0.00001, 'name': 'Contact Rate (ε)', 'format': '%.5f'},
    'k': {'min_value': 0.0001, 'max_value': 0.01, 'value': 0.001, 'step': 0.0001, 'name': 'Saturation Constant (k)', 'format': '%.4f'},
    'psi': {'min_value': 0.001, 'max_value': 0.1, 'value': 0.01, 'step': 0.001, 'name': 'Immunity Loss Rate (ψ)', 'format': '%.3f'},
    'gamma': {'min_value': 0.1, 'max_value': 0.5, 'value': 0.2, 'step': 0.01, 'name': 'Progression Rate (γ)'},
    'rho': {'min_value': 0.0001, 'max_value': 0.01, 'value': 0.001, 'step': 0.0001, 'name': 'Max Treatment Rate (ρ)', 'format': '%.4f'},
    'alpha': {'min_value': 0.001, 'max_value': 0.01, 'value': 0.006, 'step': 0.0001, 'name': 'Hospitalization Rate (α)', 'format': '%.4f'},
    'delta': {'min_value': 0.001, 'max_value': 0.01, 'value': 0.0024, 'step': 0.0001, 'name': 'Disease Death Rate (δ)', 'format': '%.4f'},
    'tau': {'min_value': 0.001, 'max_value': 0.01, 'value': 0.00219, 'step': 0.0001, 'name': 'Natural Recovery Rate (τ)', 'format': '%.5f'},
    'mu': {'min_value': 0.01, 'max_value': 0.2, 'value': 0.1, 'step': 0.01, 'name': 'Hospital Recovery Rate (μ)'},
    'beta': {'min_value': 0.01, 'max_value': 0.1, 'value': 0.05, 'step': 0.01, 'name': 'Hospital Death Rate (β)'},
    'phi': {'min_value': 0.0001, 'max_value': 0.001, 'value': 0.00027, 'step': 0.00001, 'name': 'Bacteria Shedding Rate (φ)', 'format': '%.5f'},
    'eta': {'min_value': 0.001, 'max_value': 0.01, 'value': 0.0025, 'step': 0.001, 'name': 'Bacteria Decay Rate (η)', 'format': '%.4f'},
}

for key, config in param_definitions.items():
    params[key] = st.sidebar.slider(
        config['name'],
        min_value=config['min_value'],
        max_value=config['max_value'],
        value=config['value'],
        step=config['step'],
        format=config.get('format', '%.2f')
    )

# --- Simulation Execution ---
if st.sidebar.button('Run Simulation'):
    # --- Initial Conditions ---
    total_pop = 1_000_000
    initial_conditions = [
        total_pop - 1,  # S
        0,              # E
        1,              # I
        0,              # R
        0,              # H
        0,              # D
        1               # B
    ]

    # --- Time Span ---
    t_span = np.linspace(0, 365, 500)

    # --- Run Simulation ---
    simulator = ModelSimulator(params, initial_conditions, t_span)
    solution = simulator.run()

    # --- Prepare Results for Charting ---
    results_df = pd.DataFrame(solution, columns=['Susceptible', 'Exposed', 'Infected', 'Recovered', 'Hospitalized', 'Deceased', 'Bacteria'])
    results_df['Time'] = t_span
    results_df.set_index('Time', inplace=True)

    st.header('Simulation Results')
    st.line_chart(results_df[['Susceptible', 'Exposed', 'Infected', 'Recovered', 'Hospitalized', 'Deceased']])

    st.header('Raw Data')
    st.dataframe(results_df)
else:
    st.info('Adjust the parameters in the sidebar and click "Run Simulation" to see the results.')
