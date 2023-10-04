import scikit_posthocs as sp
from scipy import stats
import pandas as pd
from collections import defaultdict


ivp = '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/tracking_accuracy/230905_in-vivo_track-accuracy_data.csv'
evp = '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/tracking_accuracy/230904_ex-vivo_track-accuracy_data.csv'
save_data_dir = '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/tracking_accuracy'

# ---------
# Functions
# ---------

def KW_and_Dunn(df, vars, group_col='condition_key'):
    data = defaultdict(list)
    groups = []
    for k, grp in df.groupby(group_col):
        groups.append(k)
        for v in vars:
            d = grp[v].values
            data[v].append(d)
    for v in vars:
        print(f'Means and SEMs {v} for groups:')
        for i, g in enumerate(groups):
            print(g)
            print('Mean: ', data[v][i].mean())
            print('SEM: ', stats.sem(data[v][i]))
            print('n: ', len(data[v][i]))
        print(f'Kruskal Wallis for {v}')
        anova = stats.kruskal(*data[v])
        print(anova)
        print(f'Dunns test for {v}')
        ph = sp.posthoc_dunn(data[v], p_adjust='bonferroni')
        print(ph)


def mannwhitneyu(df, vars, group_col='condition_key'):
    data = defaultdict(list)
    groups = []
    for k, grp in df.groupby(group_col):
        groups.append(k)
        for v in vars:
            d = grp[v].values
            data[v].append(d)
    for v in vars:
        print(f'Means and SEMs of {v} for groups:')
        for i, g in enumerate(groups):
            print(g)
            print('Mean: ', data[v][i].mean())
            print('SEM: ', stats.sem(data[v][i]))
            print('n: ', len(data[v][i]))
        print(f'Mann Whitney for {v}')
        mwu = stats.mannwhitneyu(data[v][0], data[v][1])
        print(mwu)




# -------
# In vivo
# -------

#ivdf = pd.read_csv(ivp)
#vars = ['ID swap rate (error/frame)', 'discontinuation rate (error/frame)']
#KW_and_Dunn(ivdf, vars)

#Means and SEMs ID swap rate (error/frame) for groups:
#large
#Mean:  0.0034476568405139812
#SEM:  0.0017489616404266443
#medium
#Mean:  0.004500688340569731
#SEM:  0.0019902930433775786
#small
#Mean:  0.0008223684210526312
#SEM:  0.0008223684210526312

# Kruskal Wallis for ID swap rate (error/frame)
# KruskalResult(statistic=3.1060185685931114, pvalue=0.21161021940559366)
#Dunns test for ID swap rate (error/frame)
#          1         2         3
# 1  1.000000  1.000000  0.842767
# 2  1.000000  1.000000  0.239125
# 3  0.842767  0.239125  1.000000

#Means and SEMs discontinuation rate (error/frame) for groups:
#large 70
#Mean:  0.006208125834065682
#SEM:  0.002997718255541339
#medium 71
#Mean:  0.007226341733383984
#SEM:  0.0027062056191583844
#small 64
#Mean:  0.0
#SEM:  0.0

# Kruskal Wallis for discontinuation rate (error/frame)
# KruskalResult(statistic=6.390129686786153, pvalue=0.040963869053698414)
# Dunns test for discontinuation rate (error/frame)
#          1         2         3
# 1  1.000000  1.000000  0.135158
# 2  1.000000  1.000000  0.054456
# 3  0.135158  0.054456  1.000000
#

# -------
# Ex vivo
# -------

#evdf = pd.read_csv(evp)
#vars = ['ID swap rate (error/frame)', 'discontinuation rate (error/frame)']
#mannwhitneyu(evdf, vars)


#Means and SEMs of ID swap rate (error/frame) for groups:
#human 46
#Mean:  0.00760074508200445
#SEM:  0.004541836760862101
#mouse 34
#Mean:  0.01034858387799564
#SEM:  0.006116024424252663
# Mann Whitney for ID swap rate (error/frame)
# MannwhitneyuResult(statistic=779.0, pvalue=0.9604066432994369)

#Means and SEMs of discontinuation rate (error/frame) for groups:
#human
#Mean:  0.008103119944993124
#SEM:  0.004365781952614245
#mouse
#Mean:  0.007167260843731429
#SEM:  0.004284832677092565
# Mann Whitney for discontinuation rate (error/frame)
# MannwhitneyuResult(statistic=796.5, pvalue=0.7935304403312438)


# -------------------
# Downstream analysis
# -------------------

p = '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/tracking_accuracy/230922_in-vivo_ex-vivo_vel_yvel-elong_box.csv_data.csv'
df = pd.read_csv(p)

df_min1 = df[df['minute'] == 1]
df_min1_iv = df_min1[df_min1['type'] == 'in vivo']
df_min1_ev = df_min1[df_min1['type'] == '600 s-1']

df_min3 = df[df['minute'] == 3]
df_min3_iv = df_min3[df_min3['type'] == 'in vivo']
df_min3_ev = df_min3[df_min3['type'] == '600 s-1']
print('n in vivo = ', len(df_min3_iv))
print('n ex vivo = ', len(df_min3_ev))

r0 = stats.mannwhitneyu(df_min1_iv['dv'].values, df_min1_ev['dv'].values)
print('Min 1: dv: ', r0)

r1 = stats.mannwhitneyu(df_min1_iv['dvy'].values, df_min1_ev['dvy'].values)
print('Min 1: dvy: ', r1)

r2 = stats.mannwhitneyu(df_min3_iv['elong'].values, df_min3_ev['elong'].values)
print('Min 3: elong: ', r2)

r3 = stats.mannwhitneyu(df_min1_iv['elong'].values, df_min1_ev['elong'].values)
print('Min 1: elong: ', r3)

#Min 1: dv:  MannwhitneyuResult(statistic=48.0, pvalue=0.001098901098901099)
#Min 1: dvy:  MannwhitneyuResult(statistic=45.0, pvalue=0.007692307692307693)
#Min 3: elong:  MannwhitneyuResult(statistic=48.0, pvalue=0.001098901098901099)

# 600 is
# Min 1: dv:  MannwhitneyuResult(statistic=48.0, pvalue=0.001098901098901099)
# Min 1: dvy:  MannwhitneyuResult(statistic=41.0, pvalue=0.04175824175824176)
# Min 3: elong:  MannwhitneyuResult(statistic=36.0, pvalue=0.17032967032967034)
# Min 1: elong:  MannwhitneyuResult(statistic=0.0, pvalue=0.001098901098901099)