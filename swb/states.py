# Copyright (C) 2013-2018  TEI of Epirus
# Copyright (C) 2018-2019  University of Ioannina
# GNU General Public License. See LICENSE

def _taw(fc, wp):
    return fc - wp

def _raw(p, taw):
    return p * taw

def get_ro(peff, theta_s, theta_1):
    if theta_1 - theta_s + peff <= 0:
        return 0.0
    return theta_1 - theta_s + peff

def get_dp(peff, theta_1, fc, draintime):
    if theta_1 - fc + peff < 0:
        return 0.0
    return (theta_1 - fc + peff) / draintime

def get_ks(dr, taw, raw):
    if (taw - dr) / (taw - raw) > 1:
        return 1
    return (taw - dr) / (taw - raw)

def get_crop_evapotranspiration(evap, kc, ks):
    return evap * ks * kc

def get_inet(dr, fc_irt, raw, net_event):
    if net_event:
        return 0.0
    if dr > raw:
        return dr * fc_irt
    return 0.0

def get_dr_1(dr, taw, inet=None):
    if not inet:
        return 0.0
    if dr - inet > taw:
        return taw
    return dr - inet

def get_theta(theta_init, theta_s, fc, dr, inet=None):
    if not inet:
        inet = 0.0
    if theta_init - dr >= theta_s:
        return theta_s
    return fc - dr + inet

## Not used anymore
def covert2mm(value, rd, rd_factor):
    return value * rd * rd_factor

def get_draintime(rd, a, b):
    return a * (rd * 100) ** b
