import pandas as pd


def get_tracks_scale(df):
    um_cols = ['zs', 'ys', 'xs']
    px_cols = ['z_pixels', 'y_pixels', 'x_pixels']
    scale = [1, ]
    for px, um in zip(px_cols, um_cols):
        px_val = df[px].values[0]
        i = 0
        while px_val == 0.0:
            i += 1
            px_val = df[px].values[i]
        px_d = df[px].values[i + 1] - px_val
        um_d = df[um].values[i + 1] - df[um].values[i]
        s = um_d / px_d
        scale.append(s)
    return scale


p = '/Users/abigailmcgovern/Data/iterseg/sample_data/tracks_for_annotation/tracks/201118_HxV_600is.parquet'
df = pd.read_parquet(p)

get_tracks_scale(df)