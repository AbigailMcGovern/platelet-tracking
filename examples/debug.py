from platetrack.dock_widgets import _track_platelets
import napari
import zarr
from pathlib import Path

example_root = Path('/Users/abigailmcgovern/Data/iterseg/sample_data/annotrack_example/')

sp = example_root / 'segmentations/230824_HxV3000is_plateseg2c.zarr'
ip = example_root / 'images/201118_hTR4_DMSO_3000s_.zarr'


napari_viewer = napari.Viewer()

s = zarr.open(sp)
napari_viewer.add_labels(s, scale=(1, 2, .5, .5), name='seg')

ims = zarr.open(ip)
for i in range(4):
    napari_viewer.add_image(ims[i, ...], name=f'img_{i}', scale=(1, 2, .5, .5))

labels_layer = napari_viewer.layers['seg']
image_layer = None
use_all_image_layers = True
sample_name = 'mishterman'
treatment_name = 'nothingsir'
units = 'um'
save_file = example_root / 'out-platetrack/debug.parquet'
save_mode = 'append'
save_format = 'parquet'
search_range = 2
xy_origin = 'centre'
rotation = 45

_track_platelets(napari_viewer, labels_layer, image_layer,
                     use_all_image_layers, sample_name, treatment_name, units,
                     save_file, save_mode,
                     save_format, search_range, xy_origin, rotation)