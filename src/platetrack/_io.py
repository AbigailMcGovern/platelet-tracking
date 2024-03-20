from __future__ import annotations  # needed for arg: Type1 | Type2
import os
import pathlib
import string
import warnings
import numpy as np
import pandas as pd
from pathlib import Path


def load_tracks(path: pathlib.Path | str):
    """Read tracks in from path."""
    layer_type = 'tracks'
    if path.endswith('.parquet'):
        df = pd.read_parquet(path)
    elif path.endswith('.csv'):
        df = pd.read_csv(path)
    scale, cols = get_tracks_scale_and_cols(df)
    data = df[cols].values
    layer_meta = {
        'scale' : scale, 
        'properties' : df, 
        'name' : Path(path).stem
    }
    return [(data, layer_meta, layer_type)]


def get_napari_reader(path):
    if path.endswith('.csv') or path.endswith('.parquet'):
        return load_tracks
    return None


def get_tracks_scale_and_cols(df):
    pixel_coords_cols = ['frame', 'z_pixels', 'y_pixels', 'x_pixels']
    data_coords_cols = [
            't', 'z_pixels_scaled', 'y_pixels_scaled', 'x_pixels_scaled'
            ]
    id_col = ['particle']
    # this code assumes *no* translation
    scale = [1,] * 4
    for i, (px, dt) in enumerate(zip(pixel_coords_cols, data_coords_cols)):
        if dt in df:
            first_nonzero = np.flatnonzero(df[dt])[0]
            scale[i] = df[dt][first_nonzero] / df[px][first_nonzero]
    cols = id_col + pixel_coords_cols
    return scale, cols


# ['pid', 'index', 'z_pixels', 'y_pixels', 'x_pixels',
#  'inertia_tensor_eigvals-0', 'inertia_tensor_eigvals-1',
#  'inertia_tensor_eigvals-2', 'area', 'images [2]: mean_intensity',
#  'images [2]: max_intensity', 'frame', 'label', 'zs', 'ys', 'xs',
#  'volume', 'elongation', 'flatness', 'sample_name', 'treatment',
#  'time_processed', 'particle', 'nrtracks', 'dvx', 'dvy', 'dvz',
#  'dv', 'tracknr', 'nb_particles_15', 'nb_disp_15', 'nb_density_15']