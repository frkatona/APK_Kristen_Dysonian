import numpy as np
import lmfit
import plotly.graph_objects as go

# Define the Dysonian function for EPR spectrum
def dysonian(x, A, B, g, delta_g):
    absorptive = A * ((x - g) / (delta_g + (x - g)**2))
    dispersive = B * ((delta_g) / (delta_g + (x - g)**2))
    return absorptive + dispersive

# Create a model from the Dysonian function
dysonian_model = lmfit.Model(dysonian)

# Generate some example data (using hypothetical parameters for demonstration)
x = np.linspace(-10, 10, 100)
true_A, true_B, true_g, true_delta_g = 1, 0.5, 0, 2
y = dysonian(x, true_A, true_B, true_g, true_delta_g) + np.random.normal(scale=0.1, size=len(x))/10

# Initial parameter guess
params = dysonian_model.make_params(A=1, B=1, g=0, delta_g=1)

# Fit the model to the data
result = dysonian_model.fit(y, params, x=x)

# Print the fit report
print(result.fit_report())

# Plot the data and the fit
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data'))
fig.add_trace(go.Scatter(x=x, y=result.best_fit, mode='lines', name='Fit'))
fig.show()