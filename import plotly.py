import plotly.graph_objects as go
import pandas as pd

# 1. Your Belt Thickness Data
belt_thickness_data = [
    1.084, 1.078, 1.101, 1.090, 1.087, 1.082, 1.096, 1.074, 1.065, 1.082,
    1.062, 1.083, 1.094, 1.103, 1.058, 1.101, 1.053, 1.099, 1.075, 1.092,
    1.104, 1.101, 1.101, 1.071, 1.095, 1.085, 1.067, 1.126, 1.094, 1.093,
    1.071, 1.075, 1.069, 1.082, 1.098, 1.089, 1.089, 1.071, 1.088, 1.061,
    1.082, 1.069, 1.086, 1.085, 1.050, 1.094, 1.062, 1.089, 1.062, 1.079,
    1.079, 1.062, 1.089, 1.050, 1.083, 1.062, 1.071, 1.087, 1.055, 1.085,
    1.101, 1.079, 1.075, 1.070, 1.095, 1.053, 1.088, 1.078, 1.061, 1.090,
    1.093, 1.045, 1.092, 1.077, 1.088, 1.092, 1.036, 1.095, 1.079, 1.089,
    1.074, 1.069, 1.090, 1.078, 1.088, 1.062, 1.073, 1.083, 1.084, 1.094,
    1.076, 1.061, 1.056, 1.083, 1.102, 1.089, 1.086, 1.085, 1.086, 1.093,
    1.043, 1.088, 1.091, 1.085, 1.103, 1.071, 1.093, 1.069, 1.083, 1.060,
    1.079, 1.122, 1.088, 1.100, 1.059, 1.073, 1.060, 1.090, 1.083, 1.090,
    1.085, 1.071, 1.082, 1.082, 1.094, 1.094, 1.069, 1.109, 1.059, 1.097,
    1.071, 1.089, 1.094, 1.084, 1.082, 1.089, 1.101, 1.071, 1.084, 1.063,
    1.069, 1.070, 1.087, 1.082, 1.062, 1.070, 1.077, 1.071, 1.069, 1.065,
    1.090, 1.062, 1.087, 1.057, 1.084, 1.060, 1.079, 1.098, 1.051, 1.085,
    1.058, 1.090, 1.080, 1.079, 1.090, 1.039, 1.106
]

# 2. Setup Data
df = pd.DataFrame({'Thickness': belt_thickness_data})

# Calculate Average Curve (Moving Average flows through the data)
df['Average_Curve'] = df['Thickness'].rolling(window=10, min_periods=1).mean()

# Identify Peaks (Points higher than the ones directly before and after them)
is_peak = (df['Thickness'] > df['Thickness'].shift(1)) & (df['Thickness'] > df['Thickness'].shift(-1))
peaks_df = df[is_peak]

# Identify Lows (Points lower than the ones directly before and after them)
is_low = (df['Thickness'] < df['Thickness'].shift(1)) & (df['Thickness'] < df['Thickness'].shift(-1))
lows_df = df[is_low]

# 3. Create the interactive figure
fig = go.Figure()

# --- Trace 0: Raw Data ---
fig.add_trace(go.Scatter(
    x=df.index, y=df['Thickness'],
    mode='lines+markers', name='Raw Thickness Data',
    line=dict(color='lightgray', width=1),
    marker=dict(size=4, color='gray')
))

# --- Trace 1: Average Curve ---
fig.add_trace(go.Scatter(
    x=df.index, y=df['Average_Curve'],
    mode='lines', name='Average Curve (Moving Trend)',
    line=dict(color='blue', width=2.5)
))

# --- Trace 2: Peak Curve (Upper Envelope) ---
fig.add_trace(go.Scatter(
    x=peaks_df.index, y=peaks_df['Thickness'],
    mode='lines+markers', name='Peak Curve (Upper Envelope)',
    line=dict(color='red', width=2, shape='spline'), # Spline makes the curve smooth between points
    marker=dict(size=6, color='red')
))

# --- Trace 3: Low Curve (Lower Envelope) ---
fig.add_trace(go.Scatter(
    x=lows_df.index, y=lows_df['Thickness'],
    mode='lines+markers', name='Low Curve (Lower Envelope)',
    line=dict(color='green', width=2, shape='spline'),
    marker=dict(size=6, color='green')
))

# 4. Add Dropdown Menu for View Modes
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Show All",
                     method="update",
                     args=[{"visible": [True, True, True, True]}]),
                dict(label="Raw Data Only",
                     method="update",
                     args=[{"visible": [True, False, False, False]}]),
                dict(label="Peak & Low Envelopes",
                     method="update",
                     args=[{"visible": [True, False, True, True]}]),
                dict(label="Average Trend Only",
                     method="update",
                     args=[{"visible": [True, True, False, False]}]),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.01,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )
    ],
    title='Interactive Belt Thickness Chart (Envelopes)',
    xaxis_title='Sample Number',
    yaxis_title='Thickness',
    hovermode="x unified",
    template="plotly_white",
    # Move legend outside to the right so it doesn't overlap the lines
    legend=dict(
        yanchor="top", y=1,
        xanchor="left", x=1.02
    )
)

# 5. Export to HTML
output_filename = "belt_thickness_envelopes.html"
fig.write_html(output_filename)

print(f"Success! The updated chart has been saved as '{output_filename}'.")