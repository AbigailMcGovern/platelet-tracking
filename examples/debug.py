from platetrack.dock_widgets import _track_platelets
import napari
import numpy as np
import zarr



napari_viewer = napari.Viewer()

sp = '/Users/abigailmcgovern/Data/iterseg/sample_data/annotrack_example/segmentations/230824_HxV3000is_plateseg2c.zarr'
s = zarr.open(sp)
napari_viewer.add_labels(s, scale=(1, 2, .5, .5), name='seg')

ip = '/Users/abigailmcgovern/Data/iterseg/sample_data/annotrack_example/images/201118_hTR4_DMSO_3000s_.zarr'
ims = zarr.open(ip)
for i in range(4):
    napari_viewer.add_image(ims[i, ...], name=f'img_{i}', scale=(1, 2, .5, .5))

labels_layer = napari_viewer.layers['seg']

image_layer = None


use_all_image_layers = True

sample_name = 'mishterman'
treatment_name = 'nothingsir'
x_microns, y_microns, z_microns = 0.5, 0.5, 2
save_dir = '/Users/abigailmcgovern/Data/iterseg/sample_data/mics'
save_file = None
save_format = 'parquet'
search_range = 2
xy_origin = 'centre'
rotation = 45

_track_platelets(napari_viewer, labels_layer, image_layer,
                     use_all_image_layers, sample_name, treatment_name, 
                     x_microns, y_microns, z_microns, save_dir, save_file, 
                     save_format, search_range, xy_origin, rotation)