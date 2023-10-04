from iterseg._dock_widgets import _load_data
import napari
import pandas as pd


ip = '/Users/abigailmcgovern/Data/platelet-analysis/P-selectin/211021_IVMTR139_Inj3_DMSO_exp3.zarr'

v = napari.Viewer()

_load_data(v, directory=ip, data_type='individual frames', 
           layer_name='images', layer_type='Image', 
           scale=(2, 0.5, 0.5), translate=(0, 0, 0), split_channels=True)

napari.run()