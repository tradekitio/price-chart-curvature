# Core Imports
# Need to add license here.
import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import normalize

# Extra plotly bits.
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

# Local Imports
import utils as u

# CSV importing sage.
print('Importing data as CSV.')
df = pd.read_csv('./data/data.csv')

# ;-------------------------------------------------------------------
# ; Prepare Data
# ;-------------------------------------------------------------------

# Specify a range
range_index_in = df.loc[df['date_label']=='2017-03-05 10:00:00'].index.values[0]
range_index_out = df.loc[df['date_label']=='2017-03-12 22:00:00'].index.values[0]

# Perform the slicing based on the provided time-frame.
my_date_range = df[range_index_in:range_index_out+1]

# Copy the required bits into a new data-set
data_slice = my_date_range[['timestamp', 'date', 'close']].copy()
data_slice.index = my_date_range.index

# Resample the incoming data-slice.
data_slice_resampled = u.resample_data(
        data_slice,
        input_timeframe='2H',
        output_timeframe='4H',
        smooth=True,
        smoothing_length=2
        )

print data_slice_resampled.tail()

# Convert timestamp to floats
data_slice_resampled['time_as_float'] = data_slice_resampled.timestamp.values.astype(float)

# Create an intermediate numpy array.
x = data_slice_resampled[['time_as_float', 'smooth_close']].values

# Calculate Curvature
b = u.get_curvature(x)

# Use a temp data-frame to store the results of the curvature calculations.
tmp_df = b

# Normalize the results of curvature solution.
tmp_df[:, [-1]] = normalize(tmp_df[:, -1, None], norm='max', axis=0)

# Add the solution data to our main data-frame.
data_slice_resampled['solution'] = tmp_df[:, 1]

# ;-------------------------------------------------------------------
# ; TRACE
# ;---------------------------------------------------------------------------------
# Create the candlestick plotter.
trace_candlestick = go.Candlestick(
        x = my_date_range['date_label'],
        open = my_date_range['open'],
        high = my_date_range['high'],
        low = my_date_range['low'],
        close = my_date_range['close'],
        opacity = 1.0,
        )

# Tracer price closing line.
trace_close = go.Scatter(
        x = my_date_range['date_label'],
        y = my_date_range['close'],
        mode = 'lines',
        name = 'Price Close',
        opacity = 0.4,
        line = dict(
            shape='line',
            color = ('rgb(205, 12, 24)'),
            width = 1)
        )

# Interpolated price closing data.
trace_resampled = go.Scatter(
        x = data_slice_resampled['date'],
        y = data_slice_resampled['smooth_close'],
        mode = 'lines',
        name = 'Smooth Spline',
        opacity = 1.0,
        line = dict(
            shape='spline',
            color = ('rgb(1,196,226)'),
            width = 2)
        )

# Trace Curvature as scatter
trace_curvature = go.Scatter(
        x = data_slice_resampled['date'],
        y = data_slice_resampled['solution'],
        mode = 'markers',
        name = 'Curvature',
        hoverinfo = 'skip',
        opacity = 1.0,
        legendgroup = 'curvature',
        showlegend = False,
        line = dict(
            shape='spline',
            color = ('rgb(153, 51, 255)'),
            width = 1)
        )

# Trace Curvature as bars
trace_volatility = go.Bar(
        x = data_slice_resampled['date'],
        y = data_slice_resampled['solution'],
        name = 'Curvature',
        legendgroup = 'curvature',
        opacity = 0.5,
        width = 4000000
        )

# Initial figure layout.
fig = tools.make_subplots(
        shared_xaxes=True,
        rows=3,
        cols=1,
        subplot_titles=('Candles', 'Data', 'Curvature')
        )

# Insert sub-plots.
fig.append_trace(trace_candlestick, 1, 1)
fig.append_trace(trace_close, 2, 1)
fig.append_trace(trace_resampled, 2, 1)
fig.append_trace(trace_volatility, 3, 1)
fig.append_trace(trace_curvature, 3, 1)

# Prepare layout.
layout = go.Layout(
        xaxis=dict(
            fixedrange=True,
            domain=[0, 1],
            ),
        yaxis1=dict(
            fixedrange=True,
            domain=[0, 0.6]
            ),
        yaxis2=dict(
            fixedrange=True,
            domain=[0.6, 0.8]
            ),
        yaxis3=dict(
            fixedrange=True,
            domain=[0.8, 1]
            ),
        )
# Modify the layout
# fig['layout'].update(height=800, width=800, title='')

# Plot
plotly.offline.plot(fig, filename='./html/plot-data.html')
