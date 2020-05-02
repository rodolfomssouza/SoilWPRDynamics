#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
Dynamics of soil penetration resistance in water-controlled
environment

doi:

This code simulates the soil water balance and penetration resistance
in water-controlled environments given the daily rainfall and soil parameters.

Rodolfo Souza et al.
Last edit: 2020-04-30

Models (module)

"""

__author__ = "Rodolfo Souza"
__email__ = "rodolfosouza@usp.br"
__date__ = "2020-04-30"
__license__ = "GPL"
__version__ = "1.0.0"

# Packages -------------------------------------------------------------------
import numpy as np
import pandas as pd
from tqdm import tqdm


# Class ----------------------------------------------------------------------
class Soil:

    def __init__(self, s=None, rain=None, dt=None, rains=None, **kwargs):
        """
        This class runs a simple soil water balance model in order to
        simulate the soil moisture, evapotranspiration, leakage, and
        runoff, based on daily rainfall data and some soil parameters.

        :param s: initial value of soil moisture [-].
        :param rain: rainfall value.
        :param dt: time step to solve the model. Default is 1/48.
        :param rains: rainfall time series at daily scale.
        :param kwargs: a dictionary with all parameters needed to
                       run the model. Ex.:

                    soilpar = {'sh': 0.11,     # s at hygroscopic point
                               'sw': 0.15,     # s at wilting point
                               'sstar': 0.28,  # s below field capacity [s*]
                               'sfc': 0.30,    # s at field capacity
                               'ks': 201,      # hydraulic conductivity
                               'phi': 4.05,    # exponent of retention curve
                               'zr': 40,       # soil depth
                               'n': 0.37,      # porosity
                               'emax': 0.50,   # maximum ET
                               'ew': 0.05,     # evaporation rate
                               'a': -5.76,     # parameter a of PR model
                               'b': 5.63,      # parameter b of PR model
                               'c': -15.32,    # parameter c of PR model
                               'bd': 1.68      # bulk density
                       }

        :return: soil water balance and penetration resistance
                 depending of the methods called.
        """
        self.s = s
        self.rain = rain
        self.dt = dt
        self.rains = rains
        self.p = kwargs
        print("Soil water balance and penetration resistance modeling")

    def soil_dryness(self, s0):
        """
        This function returns the time (days) of the soil dryness
        for a given initial condition of soil moisture greater
        than soil moisture at field capacity.

        :return: the time in days to reach soil moisture at some levels.
        """
        p = self.p
        beta = 2 * p['phi'] + 4
        m = p['ks'] / (p['n'] * p['zr'] * (np.exp(beta * (1 - p['sfc'])) - 1))
        etaw = p['ew'] / (p['n'] * p['zr'])
        eta = p['emax'] / (p['n'] * p['zr'])

        if s0 <= p['sfc']:
            tsfc = 0
        else:
            tsfc = (1 / (beta * (m - eta))) * (beta * (p['sfc'] - s0) + np.log(
                (eta - m + m * np.exp(beta * (s0 - p['sfc']))) / eta))
        tsstar = ((p['sfc'] - p['sstar']) / eta) + tsfc
        tsw = ((p['sstar'] - p['sw']) / (eta - etaw)) * np.log(eta / etaw) + tsstar
        stime = dict(tsfc=np.round(tsfc, 3), tsstar=np.round(tsstar, 3), tsw=np.round(tsw, 3))

        print(f'\nDryness time with soil moisture starting at {s0:.2f}:\n'
              f'reach field capacity: {tsfc:.2f} days;\n'
              f'reach sstar: {tsstar:=13.2f} days;\n'
              f'reach wilting point: {tsw:=5.2f} days.')
        return stime

    def swb(self):
        """
        Runs the soil water balance model for each component and
        returns a dictionary with daily simulation.

        :return: the water balance components (s, ET, Lk, and Q)
        at daily scale.
        """
        s = self.s
        p = self.p
        if self.dt is None:
            dt = 1 / 48
        else:
            dt = self.dt
        nr = int(np.round(1 / dt, 0))
        swsc = p['n'] * p['zr']
        sr = []
        et = []
        lk = []
        qr = []
        for i in np.arange(nr):
            # q = 0
            if i == 0:
                if self.rain is None:
                    self.rain = 0
                else:
                    self.rain = self.rain
                rain = self.rain
            else:
                rain = 0

            s_in = s + rain / swsc
            if s_in > 1.0:
                q = (s_in - 1.0) * swsc
                s_in = 1.0
            else:
                q = 0
            etr = (Soil.evapotranspiration(self) / swsc) * dt
            lkr = (Soil.leakage(self) / swsc) * dt
            s = s_in - (etr + lkr)
            # print(s)
            sr.append(s)
            et.append(etr * swsc)
            lk.append(lkr * swsc)
            qr.append(q)
            self.s = sr[-1]
        rswb = dict(sr=sr[-1], rain=self.rain, s=np.mean(sr), ET=np.sum(et), Lk=np.sum(lk), Q=np.sum(qr))
        return rswb

    def evapotranspiration(self):
        """
        Compute the Evapotranspiration (ET) based on soil moisture.

        :return: the daily evapotransporation in the same unit of
        rainfall. Ex.: cm/day.
        """
        s = self.s
        p = self.p
        if s < p['sw']:
            et = p['ew'] * (s - p['sh']) / (p['sw'] - p['sh'])
        elif p['sw'] < s <= p['sstar']:
            et = p['ew'] + (p['emax'] - p['ew']) * (s - p['sw']) / (p['sstar'] - p['sw'])
        else:
            et = p['emax']
        return et

    def leakage(self):
        """
        Compute the drainage based on soil moisture.

        :return: the daily drainage in the same unit of
        rainfall. Ex.: cm/day.
        """
        s = self.s
        p = self.p
        lk = p['ks'] * s ** (2 * p['phi'] + 3)
        return lk

    def swbprday(self):
        """
        Runs the soil water balance model for a rainfall series and
        compute the water balance component (s, ET, Lk, and Q) and
        the soil penetration resistance.

        :return: water balance components and soil penetration
        resistance for the same amount of days in the rainfall series.
        """
        p = self.p
        if self.s is None:
            self.s = (0.75 * p['sh'] + 1.25 * p['sw']) / 2
        else:
            self.s = self.s
        rains = self.rains
        nr = len(rains)
        s_out = np.zeros(nr)
        et_out = np.zeros(nr)
        lk_out = np.zeros(nr)
        q_out = np.zeros(nr)
        pr_out = np.zeros(nr)
        nrr = np.arange(nr)
        for i in tqdm(nrr):
            self.rain = rains[i]
            swbr = Soil.swb(self)
            self.s = swbr['sr']
            s_out[i] = np.round(swbr['s'], 4)
            et_out[i] = np.round(swbr['ET'], 4)
            lk_out[i] = np.round(swbr['Lk'], 4)
            q_out[i] = np.round(swbr['Q'], 4)
            pr_out[i] = np.round(Soil.soil_pr(self, swbr['s']), 4)
        out = pd.DataFrame({'Rain': self.rains, 's': s_out, 'ET': et_out,
                            'Lk': lk_out, 'Q': q_out, 'PR': pr_out})
        return out

    def soil_pr(self, s):
        """
        This function returns penetration resistance of soil by
        Jakobsen and Dexter (1987).

        :arg: Besides the parameters passed in the class, it is
        necessary to inform the soil moisture (s).

        :return: the soil penetration resistance in MPa.
        """
        p = self.p
        pr = np.exp(p['a'] + p['b'] * p['bd'] + p['c'] * s * p['n'])
        return pr
