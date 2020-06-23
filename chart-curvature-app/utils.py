# Core Imports
# Need to add licenses here.
import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import normalize

def module_test(test='test'):
    print test

def smooth_data(df_block,win=10):
    # Perform the smoothing op.
    smoothed = np.correlate(df_block, np.ones(win)/win, 'same')

    # Override FIRST and LAST element to prevent deformation.
    smoothed[0] = df_block.iloc[0]
    smoothed[-1] = df_block.iloc[-1]

    # Return the result.
    return smoothed

def resample_data(input_df, input_timeframe='2H', output_timeframe='4H', smooth=False, smoothing_length=2):
    # Re-assign the index.
    # Assign the 'timestamp' as the index so we can sample.
    data_slice = input_df.set_index(['timestamp'])

    # Convert the 'timestamp' into a valid date-time object.
    data_slice.index = pd.to_datetime(data_slice.index, unit='s')

    # Down-sample
    data_slice_down_sampled = data_slice.resample(output_timeframe, label='left').mean().reset_index()

    # Up-sample the downsamples.
    data_slice_up_sampled = data_slice_down_sampled.set_index('timestamp').resample(input_timeframe, label='right').mean().reset_index()

    # Interpolate NANs
    data_slice_up_sampled_interpolated = data_slice_up_sampled.interpolate(method='cubic')

    if smooth:
        # Construct a temp dataframe.
        tmp_df = pd.DataFrame({
            'x_value': data_slice_up_sampled_interpolated.timestamp.values.astype(float),
            'y_value': data_slice_up_sampled_interpolated['close'],
            })

        # Smooth the Y data.
        data_slice_up_sampled_interpolated['smooth_close'] = smooth_data(tmp_df['y_value'], win=smoothing_length)

    # Restore the index.
    data_slice_up_sampled_interpolated.index = input_df.index

    # Fix names.
    data_slice_up_sampled_interpolated.columns = ['date', 'close', 'smooth_close']

    # Re-introduce the timestamp row
    data_slice_up_sampled_interpolated['timestamp'] = input_df['timestamp']

    # Return the processed data frame.
    return data_slice_up_sampled_interpolated

def get_curvature(df_block):
    # Pass-on the data block.
    a = df_block

    # ;---------------------------------------------------------------------------------
    # ; STAGE (1): The first derivative.
    # ;---------------------------------------------------------------------------------
    # Calculate the tangents (first derivative of position, which is velocity).
    # ... split the position into the X and Y components.
    pos_x = a[:, 0]
    pos_y = a[:, 1]

    # Calculate the derivative of X (change in the X component of position).
    dx_dt = np.gradient(pos_x)
    # Calculate the derivative of Y (change in the Y component of position).
    dy_dt = np.gradient(pos_y)

    # Construct the tangents (velocity) array.
    velocity = np.array([[dx_dt[i], dy_dt[i]] for i in range(dx_dt.size)])

    # Speed (the length of the tangents)
    ds_dt = np.sqrt(dx_dt * dx_dt + dy_dt * dy_dt)

    # Normalize tangents
    tangent = np.array([1/ds_dt] * 2).transpose() * velocity

    # ;---------------------------------------------------------------------------------
    # ; STAGE (2): The second derivative
    # ;---------------------------------------------------------------------------------
    # Calculate the change in the tangents (second derivative).
    # ... split the normalized tangents into their X and Y components.
    tangent_x = tangent[:, 0]
    tangent_y = tangent[:, 1]

    # Calculate the derivative of X (change in the X component of velocity).
    deriv_tangent_x = np.gradient(tangent_x)
    # Calculate the derivative on Y (change in the Y component of velocity).
    deriv_tangent_y = np.gradient(tangent_y)

    # Construct the tangent derivatives (acceleration) array.
    dT_dt = np.array([[deriv_tangent_x[i], deriv_tangent_y[i]] for i in range(deriv_tangent_x.size)])

    # Calculate the length of the vectors.
    length_dT_dt = np.sqrt(deriv_tangent_x * deriv_tangent_x + deriv_tangent_y * deriv_tangent_y)

    # Normalize using the length and pack as an array.
    normal = np.array([1/length_dT_dt] * 2).transpose() * dT_dt

    # ;---------------------------------------------------------------------------------
    # ; STAGE (3): Calculations
    # ;---------------------------------------------------------------------------------
    # Second derivatives.
    d2s_dt2 = np.gradient(ds_dt)
    d2x_dt2 = np.gradient(dx_dt)
    d2y_dt2 = np.gradient(dy_dt)

    # Calculate the curvature.
    curvature = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5

    b = np.copy(a)

    # Hi-jack the initial dataset and inject into the Y component.
    cycle_limit = b[:, 0].size

    for i in range(cycle_limit):
        # Second column
        # (DEBUG)
        #print 'CYCLE <{:02}>'.format(i)
        val = curvature[i]
        b[:, 1][i]=val
        # (DEBUG)
        #print val

    # Return the curvature data set.
    return b
    return data_slice_up_sampled_interpolated
