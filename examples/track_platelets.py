from iterseg._dock_widgets import _load_data
from platelet_tracking.dock_widgets import _track_platelets
import napari


# ------------
# Select files
# ------------

image_file = '200910_ms2_hir_1800.zarr'
labels_file = '200910_MxV1800is_hir_plateseg2c.zarr'
species = 'mouse'
treatment_name = 'MxV_1800is'
sample_name='200910_MxV_1800is_hir'

# ---------
# Main code
# ---------

ip = f'/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/{species}/zarrs/{image_file}'
sp = f'/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/{species}/segmented_timeseries/{labels_file}'

v = napari.Viewer()

_load_data(v, directory=ip, data_type='individual frames', 
           layer_name='images', layer_type='Image', 
           scale=(2, 0.32, 0.32), translate=(0, 0, 0), split_channels=True)

_load_data(v, directory=sp, data_type='individual frames', 
           layer_name='labels', layer_type='Labels', 
           scale=(2, 0.32, 0.32), translate=(0, 0, 0))

od = f'/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/{species}/tracking'

_track_platelets(v, v.layers['labels'], v.layers['images [2]'], 
                 use_all_image_layers=False, sample_name=sample_name, 
                 treatment_name=treatment_name, save_dir=od, save_format='parquet', add_local_density=True)

napari.run()

# -------
# Options
# -------

# Human 3000 is
# -------------
# image_file = '201118_hTR4_DMSO_3000s_.zarr'
# labels_file = '230824_HxV3000is_plateseg2c.zarr'
# species = 'human'
# treatment_name='HxV_3000is'
# sample_name='201118_HxV_3000is'

# Human 600 is
# ------------
# image_file = '201118_hTR4_21335_600_.zarr'
# labels_file = '230824_HxV600is_plateseg2c.zarr'
# species = 'human'
# treatment_name = 'HxV_600is'
# sample_name='201118_HxV_600is'

# Mouse 600 is
# ------------
# image_file = '200917_Ms1_DMSO_600.zarr'
# labels_file = '230831_MxV600_DMSO_is_plateseg2c.zarr'
# species = 'mouse'
# treatment_name = 'MxV_600is'
# sample_name='200917_MxV_600is'

# Mouse 600 is CMFDA
# ------------------
# image_file = '201104_MsDT87_CMFDA10_600_exp3.zarr'
# labels_file = '230828_MxV600_CMFDA_is_plateseg2c.zarr'
# species = 'mouse'
# treatment_name = 'MxV_600is_CMFDA'
# sample_name='201104_CMFDA_MxV_600is'

# Mouse 1800 is - 1
# -----------------
#image_file = '20201015_Ms2_DMSO_1800.zarr'
#labels_file = '230828_MxV1800is_plateseg2c.zarr'
#species = 'mouse'
#treatment_name = 'MxV_1800is'
#sample_name='20201015_MxV_1800is'

# Mouse 1800 is - 2
# -----------------
#image_file = '201007_Ms2_DMSO_1800.zarr'
#labels_file = '230831_MxV1800is_2_plateseg2c.zarr'
#species = 'mouse'
#treatment_name = 'MxV_1800is'
#sample_name='201007_MxV_1800is'


# Mouse 1800 is Fas100
# --------------------
#image_file = '20201015_Ms3_Fas100_1800.zarr'
#labels_file = '20201015_MxV1800is_Fas100_plateseg2c.zarr'
#species = 'mouse'
#treatment_name = 'MxV_1800is'
#sample_name='20201015_MxV_1800is_Fas100'

# Mouse 1800 is hir
# -----------------
