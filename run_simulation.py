#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
Dynamics of soil penetration resistance in water-controlled
environment

doi:

This code simulates the soil water balance and penetration resistance
in water-controlled environments given the daily rainfall and soil parameters.

Rodolfo Souza et al.
Last edit: 2020-05-01

Run the simulation

"""

__author__ = "Rodolfo Souza"
__email__ = "rodolfosouza@usp.br"
__date__ = "2020-05-01"
__license__ = "GPL"
__version__ = "1.0.0"

# Packages -------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import spr_models as soilpr


# Import data and parameters -------------------------------------------------

# Rainfall data
raindata = pd.read_csv('data/data_rain.csv')

# Parameters
params = pd.read_csv('data/parameters_cxve.csv')

# Create a dictionary of parameters
paramsr = {'sh': params['sh'][0],          # s at hygroscopic point
           'sw': params['sw'][0],          # s at wilting point
           'sstar': params['sstar'][0],    # s below field capacity [s*]
           'sfc': params['sfc'][0],        # s at field capacity
           'ks': params['ks'][0],          # hydraulic conductivity
           'phi': params['phi'][0],        # exponent of retention curve
           'zr': params['zr'][0],          # soil depth
           'n': params['n'][0],            # porosity
           'emax': params['emax'][0],      # maximum ET
           'ew': params['ew'][0],          # evaporation rate
           'a': params['a'][0],            # parameter a of PR model
           'b': params['b'][0],            # parameter b of PR model
           'c': params['c'][0],            # parameter c of PR model
           'bd': params['bd'][0]           # bulk density
           }


# Run simulation -------------------------------------------------------------
soil_sim = soilpr.Soil(rains=raindata.rain.values, **paramsr).swbprday()
soil_sim.to_csv('results/SWB_PR_simulation_'+params['name'][0]+'.csv')

# Time of dryness
s0 = 0.5

tdry = soilpr.Soil(**paramsr).soil_dryness(s0)

# Sample of plot -------------------------------------------------------------
# Create plot for maximum 365 days
days = len(soil_sim.Rain)
if days > 365:
    days = 364
else:
    days = days

# Filter data
soil2 = soil_sim.loc[0:days]
days = soil2.index.values + 1

fig = plt.figure(figsize=(14, 14/1.618))
rect = fig.patch
rect.set_facecolor('white')

# Figure rainfall
ax1 = fig.add_subplot(411)
ax1.bar(days, soil2.Rain)
ax1.set_ylabel(r'Rain (cm)')
ax1.set_xlim([0, days[-1]+1])

# Soil moisture
ax2 = fig.add_subplot(412)
ax2.plot(days, soil2.s)
ax2.set_ylabel(r's')
ax2.set_ylim([0, 1])
ax2.set_xlim([0, days[-1]+1])

# ET and leakage
ax3 = fig.add_subplot(413)
ax3.plot(days, soil2.ET, label=r'ET')
ax3.plot(days, soil2.Lk, label=r'Lk')
ax3.set_ylabel(r'ET or Lk (cm)')
ax3.set_ylim([0, 1])
ax3.set_xlim([0, days[-1]+1])
ax3.legend()

# Penetration resistance
ax4 = fig.add_subplot(414)
ax4.plot(days, soil2.PR)
ax4.set_ylabel(r'PR (MPa)')
ax4.set_xlabel(r'Days')
ax4.set_ylim([0, 30])
ax4.set_xlim([0, days[-1]+1])

plt.tight_layout()
plt.savefig('results/Figure_sample_sim_'+params['name'][0]+'.pdf')
