import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO
from model_simulator import ModelSimulator

# --- Basic Setup ---
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# --- Web Server Routes ---
@app.route('/')
def index():
    """Serves the main dashboard."""
    return render_template('dashboard.html')

@socketio.on('run_simulation')
def handle_simulation(data):
    """Runs the simulation with parameters from the client."""
    try:
        # Convert all parameter values from strings to floats
        params = {key: float(value) for key, value in data['params'].items()}

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

        # --- Prepare and Send Results ---
        results = {
            'time': t_span.tolist(),
            'S': solution[:, 0].tolist(),
            'E': solution[:, 1].tolist(),
            'I': solution[:, 2].tolist(),
            'R': solution[:, 3].tolist(),
            'H': solution[:, 4].tolist(),
            'D': solution[:, 5].tolist(),
            'B': solution[:, 6].tolist(),
        }
        socketio.emit('simulation_result', results)
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        socketio.emit('simulation_error', {'error': str(e)})

# --- Main Execution ---
if __name__ == '__main__':
    print("Starting Flask server at http://localhost:5000")
    socketio.run(app, port=5001)