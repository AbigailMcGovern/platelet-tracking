from iterseg._dock_widgets import _load_data
import napari
import pandas as pd


ip = '/Users/abigailmcgovern/Data/platelet-analysis/demo-data/200527_IVMTR73_Inj4_saline_exp3.zarr'
sp = '/Users/abigailmcgovern/Data/platelet-analysis/demo-data/210920_141056_seg-track_200527_IVMTR73_Inj4_saline_exp3_labels.zarr'
tp = '/Users/abigailmcgovern/Data/platelet-analysis/demo-data/210920_141056_seg-track_200527_IVMTR73_Inj4_saline_exp3_platelet-coords_tracks.csv'

df = pd.read_csv(tp)
df = df[df['track_no_frames'] > 10]
track_df = df[['particle', 't', 'z_pixels', 'y_pixels', 'x_pixels']].values

v = napari.Viewer()

_load_data(v, directory=ip, data_type='individual frames', 
           layer_name='images', layer_type='Image', 
           scale=(2, 0.5, 0.5), translate=(0, 0, 0), split_channels=True)

_load_data(v, directory=sp, data_type='individual frames', 
           layer_name='labels', layer_type='Labels', 
           scale=(2, 0.5, 0.5), translate=(0, 0, 0))

v.add_tracks(track_df, name='tracks', scale=(2, 0.5, 0.5), properties=df)

napari.run()