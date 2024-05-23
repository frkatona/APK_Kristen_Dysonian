import pandas as pd
import plotly.graph_objects as go
import lmfit

# import data
csv_file = r'CSVs\subtracted_spectrum_PdSC4_6K_background6K_formatted_parameters.csv'
df = pd.read_csv(csv_file, skiprows=87, header=0, delimiter=';')

# modeling the dysonian
def dysonian(x, A, B, g, delta_g):
    absorptive = A * ((x - g) / (delta_g + (x - g)**2))
    dispersive = B * ((delta_g) / (delta_g + (x - g)**2))
    return absorptive + dispersive
dysonian_model = lmfit.Model(dysonian)

# fitting data to model
params = dysonian_model.make_params(A=-1.3e5, B=5e3, g=300, delta_g=70, min={'A': -1e9, 'B': 1, 'g': 100, 'delta_g': 1}, max={'A': 1e6, 'B': 1e6, 'g': 1e3, 'delta_g': 1e6})
result = dysonian_model.fit(df['MW_Absorption'], params, x=df['BField (mT)'], nan_policy='omit')
print(result.fit_report())
print(result.best_values)

# plotting data + fit
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['BField (mT)'], y=df['MW_Absorption'], mode='markers', name='Data'))
fig.add_trace(go.Scatter(x=df['BField (mT)'], y=result.best_fit, mode='lines', name='Fit'))
fig.show()