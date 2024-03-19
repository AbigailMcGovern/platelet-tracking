from __future__ import annotations  # needed for arg: Type1 | Type2

import pathlib

from magicgui import magic_factory
import napari
from napari.types import LayerDataTuple

from .platelet_info import track_my_platelets
from typing import Union, Literal
import pandas as pd


def _toggle_image_layers(widget):
    widget.image_layers.enabled = not widget.use_all_image_layers.value

def _on_track_platelets_init(widget):
    widget.use_all_image_layers.changed.connect(
            lambda: _toggle_image_layers(widget)
            )
    widget.use_all_image_layers.value = True


@magic_factory(
        widget_init=_on_track_platelets_init,
        save_file={'widget_type': 'FileEdit', 'mode': 'w'},
        # Select widget would be the right thing here but isn't working yet
        # See https://napari.zulipchat.com/#narrow/stream/212875-general/topic/napari.20plugin.20widget.20to.20select.20multiple.20layers/near/426494942
        # image_layers={'widget_type': 'Select'},
        image_layers={'layout': 'vertical'},
        )
def track_platelets(
        viewer: napari.Viewer,
        labels_layer: napari.layers.Labels,
        use_all_image_layers: bool,
        image_layers: list[napari.layers.Image],
        sample_name: str,
        treatment_name: str,
        save_file: pathlib.Path,
        save_mode: Literal['overwrite', 'append'] = 'append',
        save_format: Literal['parquet', 'csv'] = 'parquet',
        search_range: float = 2.,
        xy_origin: Union[str, tuple] = 'centre',
        rotation: float = 45.,
        ) -> LayerDataTuple:

    return _track_platelets(viewer, labels_layer, image_layers,
                     use_all_image_layers, sample_name, treatment_name, 
                     save_mode, save_file,
                     save_format, search_range, xy_origin, rotation)


def _track_platelets(
        viewer: napari.Viewer,
        labels_layer: napari.layers.Labels,
        image_layers: list[napari.layers.Image],
        use_all_image_layers: bool, 
        sample_name: str, 
        treatment_name: str,
        save_file: pathlib.Path,
        save_mode: Literal['overwrite', 'append'] = 'append',
        save_format: str="parquet",
        search_range: float=2., 
        xy_origin: Union[str, tuple]='centre', 
        rotation: float=45, 
        add_local_density: bool=True, 
        ) -> LayerDataTuple:

    labels = labels_layer.data
    if use_all_image_layers:
        image_layers = [
                ly for ly in viewer.layers
                if isinstance(ly, napari.layers.Image)
                ]
    image_channels_dict = {l.name: l.data for l in image_layers}
    z_microns, y_microns, x_microns = labels_layer.scale[-3:]
    df, p = track_my_platelets(labels, image_channels_dict,
                       save_file, save_mode, sample_name, treatment_name, x_microns,
                       y_microns, z_microns, save_format, search_range, xy_origin,
                       rotation, add_local_density)
    track_df = df[
            ['particle', 'frame',
             'z_pixels_scaled', 'y_pixels_scaled', 'x_pixels_scaled']
            ].to_numpy(dtype=float)
    return track_df, {'features': df, 'name': sample_name}, 'tracks'

