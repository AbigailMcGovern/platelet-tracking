import numpy as np
from tqdm import tqdm
from skimage.measure import regionprops_table
import pandas as pd
import os
from datetime import datetime
import trackpy as tp
from pathlib import Path
from plateletanalysis.variables.measure import finite_difference_derivatives
from plateletanalysis.variables.basic import tracknr_variable
from plateletanalysis.variables.transform import adjust_coordinates
from plateletanalysis.variables.neighbours import add_neighbour_lists, local_density
from typing import Union


def track_my_platelets( 
        labels: np.ndarray, 
        image_channels_dict: dict,
        save_dir: str, 
        save_file: str, 
        sample_name: str, 
        treatment_name: str,
        x_microns: float=0.32, 
        y_microns: float=0.32, 
        z_microns: float=2., 
        save_format: str="parquet", 
        search_range: float=2., 
        xy_origin: Union[str, tuple]='centre', 
        rotation: float=45, 
        add_local_density: bool=False, 
        ):
    df = platelet_info_from_segmentation(labels, image_channels_dict, 
                                         sample_name, treatment_name, 
                                         x_microns, y_microns, z_microns)
    df = track(df, search_range)
    df = add_track_len(df)
    if xy_origin == 'centre':
        xy_origin = np.array(labels.shape[-2:]) * np.array([y_microns, x_microns]) / 2
        xy_origin = tuple(xy_origin)
    elif xy_origin == 'top left':
        xy_origin = (0, 0)
    meta_df = {
        'sample_name' : [sample_name, ], 
        'roi_x' : [xy_origin[0], ], 
        'roi_y' : [xy_origin[1], ], 
    }
    meta_df = pd.DataFrame(meta_df)
    df = adjust_coordinates(df, meta_df, rot_angle=rotation, file_col='sample_name', 
                            roi_x_col='roi_x', roi_y_col='roi_y', path_col='sample_name', 
                            xs_col='xs', ys_col='ys', zs_col='zs', px_microns_col=None)
    df = finite_difference_derivatives(df, ('xs', 'ys', 'zs'), sample_col='sample_name')
    df = tracknr_variable(df, sample_col='sample_name')
    if add_local_density:
        df = add_neighbour_lists(df, sample_col='sample_name', coords=('xs', 'ys', 'zs'))
        df = local_density(df, z_max=labels.shape[-3] * z_microns, sample_col='sample_name')
    save_platelet_tracks(df, save_dir, save_file, sample_name, save_format)
    return df



def platelet_info_from_segmentation(
        labels: np.ndarray, 
        image_channels_dict: dict,
        sample_name: str, 
        treatment_name: str,
        x_microns: float=0.32, 
        y_microns: float=0.32, 
        z_microns: float=2., 
    ):
    '''
    Parameters
    ----------
    labels: 3D + t ndarray
    image_channels_dict: dict
        image_channels_dict is a dict with the channel name (str) 
        as the key and the array as the value (np.ndarray)
    save_dir: str
        The directory into which to save the outputted information. If the 
    '''
    now = datetime.now()
    dt = now.strftime("%y%m%d_%H%M%S")
    t_max = labels.shape[0]
    labs_df = []
    counter = 0
    for t in tqdm(range(t_max), desc="Obtaining platelet info"):
        l_max = np.max(labels[t])
        chans_dfs = []
        chans_started = False
        for key in image_channels_dict.keys():
            im = image_channels_dict[key][t, ...]
            im = np.array(im)
            if not chans_started:
                props = ('label', 'centroid', 'inertia_tensor_eigvals',
                               'area', 'mean_intensity', 'max_intensity')
                chans_started = True
            else:
                props = ('label', 'mean_intensity', 'max_intensity')
            df = regionprops_table(labels[t], 
                               intensity_image=im, 
                               properties=props)
            df['frame'] = [t,] * len(df['label']) 
            df = pd.DataFrame(df)
            df_labs = df['label'].values
            df = df.set_index('label')
            df = df.rename(columns={
            'mean_intensity' : f'{key}: mean_intensity',
            'max_intensity' : f'{key}: max_intensity',
            })
            chans_dfs.append(df)
        df = pd.concat(chans_dfs, axis=1)
        df['label'] = df_labs
        df_pids = [i for i in range(counter, len(df['label']) + counter)]
        counter += len(df['label'])
        df['pid'] = df_pids
        df = df.set_index('pid')
        bbb = len(df)
        df = df.loc[~df.index.duplicated(keep='first')]
        aaa = len(df)
        labs_df.append(df)
    labs_df = pd.concat(labs_df)
    cols = df.columns.values
    # rename the voxel coordinate columns
    cols = [c for c in cols if c.find('centroid') != -1]
    ax = ['z_pixels', 'y_pixels', 'x_pixels'] # this should be true after np.transpose in read_image()
    rename = {cols[i] : ax[i] for i in range(len(cols))}
    labs_df = labs_df.rename(columns=rename)
    # add coloumn with coordinates in microns
    microns = ['zs', 'ys', 'xs']
    factors = [z_microns, y_microns, x_microns]
    for m, a, f in zip(microns, ax, factors):
        labs_df[m] = labs_df[a] * f
    # add volume column (in microns)
    one_voxel = x_microns *y_microns * z_microns
    labs_df['volume'] = labs_df['area'] * one_voxel
    # get flatness (or lineness) scores
    labs_df = add_elongation(labs_df)
    labs_df = add_flatness(labs_df)
    # add file info
    labs_df['sample_name'] = sample_name
    labs_df['treatment'] = treatment_name
    labs_df['time_processed'] = dt
    return labs_df



def save_platelet_tracks(
        labs_df, 
        save_dir, 
        save_file, 
        sample_name, 
        save_format
        ):
    if save_dir is not None:
        path = os.path.join(save_dir, sample_name + f'.{save_format}')
    
    elif save_file is not None:
        if os.path.exists(save_file):
            if not save_file.endswith(save_format):
                save_format == Path(save_file).suffix
            if save_format == 'csv':
                df = pd.read_csv(save_file)
            elif save_format == 'parquet':
                df = pd.read_parquet(save_file)
            labs_df = pd.concat([df, labs_df]).reset_index(drop=True)
            path = save_file
    if save_format == 'csv':
        labs_df.to_csv(path)
    elif save_format == 'parquet':
        labs_df.to_parquet(path)


def add_elongation(df):
    df['elongation'] = np.sqrt(1 - df['inertia_tensor_eigvals-2'] / df['inertia_tensor_eigvals-0'])
    return df


def add_flatness(df):
    df['flatness'] = np.sqrt(1 - df['inertia_tensor_eigvals-2'] / df['inertia_tensor_eigvals-1'])
    return df


def track(platelets, search_range):
    linked_pc = tp.link_df(platelets, search_range, 
                           pos_columns=['xs', 'ys', 'zs'], 
                           t_column='frame', memory=1, 
                           adaptive_stop=0.5, adaptive_step=0.5)
    return linked_pc

def add_track_len(df):
    ids = df['particle'].values
    track_count = np.bincount(ids)
    df['nrtracks'] = track_count[ids]
    return df