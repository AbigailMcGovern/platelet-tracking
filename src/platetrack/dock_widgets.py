from magicgui import magic_factory
import napari
from .platelet_info import track_my_platelets
from typing import Union
import pandas as pd


@magic_factory(
    save_dir={'widget_type': 'FileEdit', 'mode' : 'd'}, 
    save_file={'widget_type': 'FileEdit'}, 
)
def track_platelets(
        napari_viewer: napari.Viewer,
        labels_layer: napari.layers.Labels, 
        image_layer: napari.layers.Image, 
        use_all_image_layers: bool, 
        sample_name: str, 
        treatment_name: str,
        x_microns: float=0.50, 
        y_microns: float=0.50, 
        z_microns: float=2., 
        save_dir: Union[str, None]=None, 
        save_file: Union[str, None]=None, 
        save_format: str="parquet", 
        search_range: float=2., 
        xy_origin: Union[str, tuple]='centre', 
        rotation: float=45, 
    ):

    _track_platelets(napari_viewer, labels_layer, image_layer, 
                     use_all_image_layers, sample_name, treatment_name, 
                     x_microns, y_microns, z_microns, save_dir, save_file, 
                     save_format, search_range, xy_origin, rotation)


def _track_platelets(
        napari_viewer: napari.Viewer,
        labels_layer: napari.layers.Labels, 
        image_layer: napari.layers.Image, 
        use_all_image_layers: bool, 
        sample_name: str, 
        treatment_name: str,
        x_microns: float=0.50, 
        y_microns: float=0.50, 
        z_microns: float=2., 
        save_dir: Union[str, None]=None, 
        save_file: Union[str, None]=None, 
        save_format: str="parquet", 
        search_range: float=2., 
        xy_origin: Union[str, tuple]='centre', 
        rotation: float=45, 
        add_local_density: bool=True, 
    ):

    labels = labels_layer.data
    if use_all_image_layers:
        image_channels_dict = {l.name : l.data for l in napari_viewer.layers \
                               if isinstance(l, napari.layers.Image)}
    else:
        image_channels_dict = {image_layer.name : image_layer.data}
    df, p = track_my_platelets(labels, image_channels_dict, save_dir, 
                       save_file, sample_name, treatment_name, x_microns, 
                       y_microns, z_microns, save_format, search_range, xy_origin, 
                       rotation, add_local_density)
    if save_format == 'parquet':
        df = pd.read_parquet(p)
    elif save_format == 'csv':
        df = pd.read_csv(p)
    track_df = df[['particle', 'frame', 'z_pixels_scaled', 'y_pixels_scaled', 'x_pixels_scaled']].values
    napari_viewer.add_tracks(data=track_df, properties=df, name=sample_name)

