# Campylobacteriosis Transmission Dynamics Dashboard

This project is an interactive web application that simulates and visualizes a mathematical model for the transmission dynamics of Campylobacteriosis. The dashboard is built with Streamlit and allows for real-time manipulation of model parameters to observe their impact on various population compartments.

## Features

- **Interactive Simulation:** Adjust model parameters using sliders and see the results instantly.
- **Dynamic Visualization:** The population dynamics are plotted on an interactive chart.
- **Data Export:** View and download the raw simulation data as a table.
- **Easy Deployment:** Built with Streamlit for simple deployment to the web.

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install the dependencies:**
    Make sure you have Python 3.8+ installed. Then, run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run streamlit_app.py
    ```

The application will open in your default web browser.

## Project Structure

- `streamlit_app.py`: The main application file containing the Streamlit UI and logic.
- `model_simulator.py`: The core simulation engine that solves the system of ordinary differential equations (ODEs).
- `requirements.txt`: A list of all the Python packages required to run the application.

## Model Overview

The simulation is based on a compartmental model that tracks the following populations:
- **S:** Susceptible
- **E:** Exposed
- **I:** Infected
- **R:** Recovered
- **H:** Hospitalized
- **D:** Deceased
- **B:** Bacteria Concentration

This dashboard provides a powerful tool for researchers and students to explore the complex dynamics of Campylobacteriosis transmission.
