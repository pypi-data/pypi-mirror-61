#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 13:58:15 2019

@author: jkl
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.ioff()
from scana2019Load import yieldData, dfeca, emDates, n2rate, string2date
from tools.gtools import scana2019Field
from tools.dfTools import dfdiff0
plt.close('all')

outputdir = '../projects/scana2019/all/image/yield/'

#%% maps
x = yieldData['grain85'].values
fig, ax = plt.subplots(figsize=(3,5))
ax.set_title('Scanalyzer NIT 2019')
cax = ax.imshow(scana2019Field(x))
fig.colorbar(cax, ax=ax, label=r'Grain Yield (85%) [t.ha$^{-1}$]')
ax.set_xticks([])
ax.set_yticks([])
fig.tight_layout()
fig.savefig(outputdir + 'yield-grain85.png')
fig.show()

x = yieldData['straw85'].values
fig, ax = plt.subplots(figsize=(3,5))
ax.set_title('Scanalyzer NIT 2019')
cax = ax.imshow(scana2019Field(x))
fig.colorbar(cax, ax=ax, label=r'Straw Yield (85%) [t.ha$^{-1}$]')
ax.set_xticks([])
ax.set_yticks([])
fig.tight_layout()
fig.savefig(outputdir + 'yield-straw85.png')
fig.show()

x = yieldData['biomass85'].values
fig, ax = plt.subplots(figsize=(3,5))
ax.set_title('Scanalyzer NIT 2019')
cax = ax.imshow(scana2019Field(x))
fig.colorbar(cax, ax=ax, label=r'Biomass (85%) [t.ha$^{-1}$]')
ax.set_xticks([])
ax.set_yticks([])
fig.tight_layout()
fig.savefig(outputdir + 'yield-biomass85.png')
fig.show()


#%% yield with nitrogen per varieties (response curve)
df = yieldData
dfg = df.groupby(['name','ntreatment'])
gmeans = dfg.mean().reset_index()
gsem = dfg.sem().reset_index()
dfm = pd.merge(gmeans, gsem, on=['name','ntreatment'],
               suffixes=('_avg','_sem'))
dfm = dfm.sort_values(['name','ntreatment'])
dfm['nval'] = [n2rate[a] for a in dfm['ntreatment']]

names = dfm['name'].unique()
fig, ax = plt.subplots()
for name in names:
    ie = dfm['name'] == name
    ax.errorbar(dfm[ie]['nval'], dfm[ie]['grain85_avg'],
                yerr=dfm[ie]['grain85_sem'], label=name, marker='.')
ax.set_xlabel('N rate [kg/ha]')
ax.set_ylabel('Grain Yield (85%) [t/ha]')
ax.legend()
fig.savefig(outputdir + 'yield-ntreatment-response.png')
fig.show()


#%% same for ECa or diff ECa ?
df = dfdiff0(dfeca, emDates)
df = df[df['depth'] == df['depth'].unique()[1]]
col = emDates[-2]

for col in emDates:
    dfg = df.groupby(['name','ntreatment'])
    gmeans = dfg.mean().reset_index()
    gsem = dfg.sem().reset_index()
    dfm = pd.merge(gmeans, gsem, on=['name','ntreatment'],
                   suffixes=('_avg','_sem'))
    dfm = dfm.sort_values(['name','ntreatment'])
    dfm['nval'] = [n2rate[a] for a in dfm['ntreatment']]
    
    names = dfm['name'].unique()
    fig, ax = plt.subplots()
    ax.set_title('ECa VCP0.71 on {:s}'.format(string2date([col])[0].strftime('%Y-%m-%d')))
    for name in names:
        ie = dfm['name'] == name
        ax.errorbar(dfm[ie]['nval'], dfm[ie][col + '_avg'],
                    yerr=dfm[ie][col + '_sem'], label=name, marker='.')
    ax.set_xlabel('N rate [kg/ha]')
    ax.set_ylabel('ECa [mS/m]')
    ax.legend()
    fig.savefig(outputdir + 'eca-ntreatment-response.png')
    fig.show()

''' not very clear response. Just after application there is a negative
trend (smaller change for the one that receive more N).
Later in the season there is a downward trend but always the N6 spikes up
compared to the trend
no trend for absolute values
'''

#%% graph for each variety, plot vs time with color for N

# similar to plotMeanTimes actually ...
