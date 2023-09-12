from iterseg._dock_widgets import _load_data
import napari
import pandas as pd


# ------------
# Select files
# ------------

image_file = '201118_hTR4_DMSO_3000s_.zarr'
labels_file = '230824_HxV3000is_plateseg2c.zarr'
tracks_file = '201118_HxV_3000is.parquet'
species = 'human'


# ---------
# Main code
# ---------

ip = f'/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/{species}/zarrs/{image_file}'
sp = f'/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/{species}/segmented_timeseries/{labels_file}'
tp = f'/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/{species}/tracking/{tracks_file}'


df = pd.read_parquet(tp)
df = df[df['nrtracks'] > 10]
track_df = df[['particle', 'frame', 'z_pixels', 'y_pixels', 'x_pixels']].values


v = napari.Viewer()

_load_data(v, directory=ip, data_type='individual frames', 
           layer_name='images', layer_type='Image', 
           scale=(2, 0.32, 0.32), translate=(0, 0, 0), split_channels=True)

_load_data(v, directory=sp, data_type='individual frames', 
           layer_name='labels', layer_type='Labels', 
           scale=(2, 0.32, 0.32), translate=(0, 0, 0))

v.add_tracks(track_df, name='tracks', scale=(2, 0.32, 0.32), properties=df)

napari.run()