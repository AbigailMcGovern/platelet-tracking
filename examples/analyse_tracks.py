import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plateletanalysis.variables.basic import time_seconds
from collections import defaultdict
import os
import numpy as np

# ---------
# Functions
# ---------

# Line plots
# ----------

def plot_count_density_yvel_over_time(ivdf, evdf, save_data_dir, save_name):
    new_data = defaultdict(list)
    new_data = add_group_data(ivdf, new_data, 'in vivo', 'path')
    new_data = add_group_data(evdf, new_data, 'ex vivo', 'sample_name')
    new_data = pd.DataFrame(new_data) # there is a row for each experiment at each timepoint
    vars = ['platelet count', 'density (/um3)', 'velocity (um/s)']
    new_data = smooth_vars(new_data, vars)
    plt.rcParams['svg.fonttype'] = 'none' # so the text will be saved with the svg - not curves
    fig, axs = plt.subplots(1, 3, sharex=True)
    axs[0].set_xlim(0, 200)
    sns.lineplot(data=new_data, x='time (s)', y='platelet count', ax=axs[0], hue='type')
    sns.lineplot(data=new_data, x='time (s)', y='density (/um3)', ax=axs[1], hue='type')
    sns.lineplot(data=new_data, x='time (s)', y='velocity (um/s)', ax=axs[2], hue='type')
    sns.despine(ax=axs[0])
    sns.despine(ax=axs[1])
    sns.despine(ax=axs[2])
    fig.set_size_inches(12, 3)
    sp_data = os.path.join(save_data_dir, save_name + '_data.csv')
    new_data.to_csv(sp_data)
    sp_plots = os.path.join(save_data_dir, save_name + '_plots.svg')
    fig.savefig(sp_plots)
    fig.subplots_adjust(right=0.97, left=0.13, bottom=0.17, top=0.97, wspace=0.45, hspace=0.3)
    plt.show()


def plot_count_density_yvel_over_time_ind(df, save_data_dir, save_name):
    new_data = defaultdict(list)
    new_data = add_group_data(df, new_data, 'ex vivo', 'sample_name')
    new_data = pd.DataFrame(new_data) # there is a row for each experiment at each timepoint
    vars = ['platelet count', 'density (/um3)', 'velocity (um/s)']
    new_data = smooth_vars(new_data, vars)
    plt.rcParams['svg.fonttype'] = 'none' # so the text will be saved with the svg - not curves
    fig, axs = plt.subplots(1, 3, sharex=True)
    sns.lineplot(data=new_data, x='time (s)', y='platelet count', ax=axs[0], hue='sample')
    sns.lineplot(data=new_data, x='time (s)', y='density (/um3)', ax=axs[1], hue='sample')
    sns.lineplot(data=new_data, x='time (s)', y='velocity (um/s)', ax=axs[2], hue='sample')
    sns.despine(ax=axs[0])
    sns.despine(ax=axs[1])
    sns.despine(ax=axs[2])
    fig.set_size_inches(12, 3)
    sp_data = os.path.join(save_data_dir, save_name + '_data.csv')
    new_data.to_csv(sp_data)
    sp_plots = os.path.join(save_data_dir, save_name + '_plots.svg')
    fig.subplots_adjust(right=0.97, left=0.13, bottom=0.17, top=0.97, wspace=0.45, hspace=0.3)
    fig.savefig(sp_plots)
    plt.show()

def add_group_data(df, new_data, type, sample_col):
    for k, grp in df.groupby(['time (s)', sample_col]):
        new_data['time (s)'].append(k[0])
        new_data['sample'].append(k[1])
        new_data['type'].append(type)
        count = count_platelets(grp)
        new_data['platelet count'].append(count)
        dens = np.nanmean(grp['nb_density_15'].values)
        new_data['density (/um3)'].append(dens)
        yvel = np.nanmean(grp['dv'].values)
        new_data['velocity (um/s)'].append(yvel)
    return new_data

def smooth_vars(df, vars):
    df = df.sort_values('time (s)')
    for v in vars:
        for k, grp in df.groupby('sample'):
            rolled = grp[v].rolling(window=6, center=False).mean()
            idxs = grp.index.values
            df.loc[idxs, v] = rolled
    return df

def count_platelets(grp):
    return len(pd.unique(grp['particle']))

def add_time_sec_td(df, td, sample_name, sample_col, frame_col):
    sml_df = df[df[sample_col] == sample_name]
    idxs = sml_df.index.values
    df.loc[idxs, 'time (s)'] = sml_df[frame_col] * td
    return df

def bin_time(df):
    df['time (s)'] = df['time (s)'].apply(time_bin)
    return df

def time_bin(t):
    mt = t % 5
    return np.round(t) #, -1)


# Bar plots
# ---------

def bar_plots_vars(ivdf, evdf, ivars, evars, save_data_dir, save_name):
    ivdf = bin_into_min(ivdf)
    evdf = bin_into_min(evdf)
    renameing = {ev : iv for iv, ev in zip(ivars, evars)}
    evdf = evdf.rename(columns=renameing)
    fig, axs = plt.subplots(1, len(ivars))
    new_data = defaultdict(list)
    new_data = add_bplot_data(ivdf, new_data, ivars, 'path', 'in_vivo')
    new_data = add_bplot_data(evdf, new_data, ivars, 'sample_name', 'ex_vivo')
    new_data = pd.DataFrame(new_data)
    new_data = new_data[new_data['minute'] <= 4.]
    new_data = new_data[new_data['minute'] > 0]
    plt.rcParams['svg.fonttype'] = 'none'
    for v, ax in zip(ivars, axs):
        sns.barplot(data=new_data, x='minute', y=v, hue='type', capsize=0.15, ax=ax)
        sns.stripplot(data=new_data, x='minute', y=v, hue='type',  ax=ax, dodge=True)
        sns.despine(ax=ax)
    fig.set_size_inches(12, 3)
    sp_data = os.path.join(save_data_dir, save_name + '_data.csv')
    new_data.to_csv(sp_data)
    fig.subplots_adjust(right=0.97, left=0.13, bottom=0.17, top=0.97, wspace=0.45, hspace=0.3)
    sp_plots = os.path.join(save_data_dir, save_name + '_plots.svg')
    fig.savefig(sp_plots)
    plt.show()




def bin_into_min(df):
    df['minute'] = df['time (s)'].apply(min_bin)
    return df


def min_bin(t):
    return np.ceil(t / 60).astype(int)


def add_bplot_data(df, new_data, vars, sample_col, sample_type):
    for k, grp in df.groupby(['minute', sample_col]):
        new_data['minute'].append(k[0])
        new_data['sample'].append(k[1])
        new_data['type'].append(sample_type)
        for v in vars:
            new_data[v].append(np.nanmean(grp[v].values))
    return new_data

# Box plots
# ---------

def box_plots_vars(ivdf, evdf, ivars, evars, save_data_dir, save_name):
    ivdf = bin_into_min(ivdf)
    evdf = bin_into_min(evdf)
    plt.rcParams['svg.fonttype'] = 'none'
    renameing = {ev : iv for iv, ev in zip(ivars, evars)}
    evdf = evdf.rename(columns=renameing)
    fig, axs = plt.subplots(1, len(ivars))
    new_data = defaultdict(list)
    new_data = add_bplot_data(ivdf, new_data, ivars, 'path', 'in_vivo')
    new_data = add_bplot_data(evdf, new_data, ivars, 'sample_name', 'ex_vivo')
    new_data = pd.DataFrame(new_data)
    new_data = new_data[new_data['minute'] <= 3]
    new_data = new_data[new_data['minute'] > 0]
    for v, ax in zip(ivars, axs):
        sns.boxplot(data=new_data, x='minute', y=v, hue='type', ax=ax)
        sns.stripplot(data=new_data, x='minute', y=v, hue='type',  ax=ax, dodge=True, edgecolor = 'white', linewidth=0.3)
        sns.despine(ax=ax)
    fig.set_size_inches(10, 3)
    sp_data = os.path.join(save_data_dir, save_name + '_data.csv')
    new_data.to_csv(sp_data)
    fig.subplots_adjust(right=0.97, left=0.068, bottom=0.17, top=0.97, wspace=0.357, hspace=0.3)
    sp_plots = os.path.join(save_data_dir, save_name + '_plots.svg')
    fig.savefig(sp_plots)
    plt.show()




# --------------
# Paths & config
# --------------
iv_tp = '/Users/abigailmcgovern/Data/platelet-analysis/dataframes/211206_veh-sq_df.parquet'
ex_tp = ['/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/mouse/tracking/20201015_MxV_1800is.parquet', 
         '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/mouse/tracking/201007_MxV_1800is.parquet', 
         '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/mouse/tracking/20201015_MxV_1800is_Fas100.parquet', 
         '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/mouse/tracking/200910_MxV_1800is_hir.parquet']
save_dir = '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/tracking_accuracy'
save_name = '230911_in-vivo_ex-vivo_count_dens_vel_TAdj.csv'
save_name_bar = '230911_in-vivo_ex-vivo_yvel-elong_z-vel.csv'
save_name_box = '230911_in-vivo_ex-vivo_vel_yvel-elong_box.csv'
ts_20201015 = 2.145
ts_201007 = 4.3885

# -------
# Compute
# -------
ivdf = pd.read_parquet(iv_tp)
#ivdf = ivdf[ivdf['nrtracks'] > 10]
evdf = [pd.read_parquet(p) for p in ex_tp]
evdf = pd.concat(evdf).reset_index(drop=True)
#evdf = evdf[evdf['nrtracks'] > 10]
evdf = add_time_sec_td(evdf, ts_20201015, '201007_MxV_1800is', 'sample_name', 'frame')
#print(evdf.columns.values)
evdf = add_time_sec_td(evdf, ts_20201015, '20201015_MxV_1800is', 'sample_name', 'frame')
evdf = add_time_sec_td(evdf, ts_20201015, '20201015_MxV_1800is_Fas100', 'sample_name', 'frame')
evdf =  add_time_sec_td(evdf, ts_20201015, '200910_MxV_1800is_hir', 'sample_name', 'frame')
evdf['dvy'] = evdf['dvy'] / .32 * 0.5
evdf['dvx'] = evdf['dvx'] / .32 * 0.5
evdf['dv'] = (evdf['dvy'] ** 2 + evdf['dvx'] ** 2 + evdf['dvz'] ** 2) ** 0.5
ivdf = bin_time(ivdf)
evdf = bin_time(evdf)
#plot_count_density_yvel_over_time(ivdf, evdf, save_dir, save_name)
#plot_count_density_yvel_over_time_ind(evdf, save_dir, save_name)
ivars = ['dv', 'dvy', 'elong']
evars = ['dv', 'dvy', 'elongation']
#bar_plots_vars(ivdf, evdf, ivars, evars, save_dir, save_name_bar)
box_plots_vars(ivdf, evdf, ivars, evars, save_dir, save_name_box)