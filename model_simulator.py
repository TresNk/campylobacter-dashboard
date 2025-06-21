import numpy as np
from scipy.integrate import odeint

class ModelSimulator:
    """
    Solves the system of ODEs for the Campylobacteriosis model.
    """

    def __init__(self, params, initial_conditions, t_span):
        """
        Initializes the simulator.
        :param params: A dictionary of model parameters.
        :param initial_conditions: A list or tuple of initial values for S, E, I, R, H, D, B.
        :param t_span: A numpy array of time points.
        """
        self.params = params
        self.initial_conditions = initial_conditions
        self.t_span = t_span

    def _odes(self, y, t):
        """
        Defines the system of differential equations.
        """
        S, E, I, R, H, D, B = y

        # Unpack parameters with default values from the user's paper
        Lambda = self.params.get('Lambda', 50)
        d = self.params.get('d', 1 / (65 * 365))
        epsilon = self.params.get('epsilon', 0.00058)
        k = self.params.get('k', 0.001)  # User to provide
        psi = self.params.get('psi', 0.01) # User to provide
        gamma = self.params.get('gamma', 0.2)
        rho = self.params.get('rho', 0.001) # User to provide
        alpha = self.params.get('alpha', 0.006) # Treatment delay / hospitalization rate
        delta = self.params.get('delta', 0.0024)
        tau = self.params.get('tau', 0.00219)
        mu = self.params.get('mu', 0.1) # User to provide
        beta = self.params.get('beta', 0.05) # User to provide
        phi = self.params.get('phi', 0.00027)
        eta = self.params.get('eta', 0.0025)

        # Non-linear incidence rate
        f_S_B = (epsilon * B * S) / (1 + k * B)
        
        # Saturated treatment function
        p_I = (rho * I) / (1 + alpha * I)

        # System of ODEs from the user's paper, with corrections for apparent typos
        dSdt = Lambda - f_S_B + psi * R - d * S
        dEdt = f_S_B - (gamma + d) * E
        dIdt = gamma * E - p_I - (alpha + d + delta + tau) * I
        dRdt = p_I + mu * H - (d + psi) * R
        dHdt = alpha * I - (mu + beta) * H
        # The paper's equation for dD/dt appears to have typos (dD instead of d*D and a missing delta*I term).
        # The equation below is based on the model description and diagram.
        dDdt = delta * I + beta * H - d * D
        dBdt = phi * I - eta * B
        
        return [dSdt, dEdt, dIdt, dRdt, dHdt, dDdt, dBdt]

    def run(self):
        """
        Runs the simulation.
        """
        solution = odeint(self._odes, self.initial_conditions, self.t_span)
        return solution
