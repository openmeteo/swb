# Copyright (C) 2013-2018  TEI of Epirus
# Copyright (C) 2018-2019  University of Ioannina
# GNU General Public License. See LICENSE


import pandas as pd
from .validators import _validate_input_series
from .states import (_taw, _raw, get_ro, get_dp, get_ks,
                      get_crop_evapotranspiration, get_inet, get_dr_1,
                      get_theta)

def calculate_soil_water(
    *,
    theta_s,
    theta_fc,
    theta_wp,
    rd,
    zr_factor,  # its not realy used, we require units to be converted by user (see below)
    kc,
    p,
    draintime,
    effective_precipitation,
    crop_evapotranspiration,  # This should be named as ET due calculations based on DR(i) (see below)
    net_irrigation,  # In case of no irrigation the value should be None (see below)
    theta_init,
    mif
):
    # Validate if pd.Series and have the same DateIndex
    _validate_input_series([
        effective_precipitation,
        crop_evapotranspiration,
        net_irrigation
    ])
    df = pd.DataFrame(
        {
            "peff": effective_precipitation,
            "et": crop_evapotranspiration,
            "net": None,
        }
    )
    CR = 0.0  # Static exists for later dev improvement

    # Note: for rd_factor
    # For example we used to use rd_factor here to convert units taw and raw.
    # Now user should pass the unit (mm) else we need flag for convertion.
    taw = _taw(theta_fc, theta_wp)
    raw = _raw(p, taw)

    for date, row in df.iterrows():
        loc = df.index.get_loc(date)

        prev_theta = df.ix[loc - 1, "theta"] if loc != 0 else theta_init
        prev_dr = df.ix[loc - 1, "dr_1"] if loc != 0 else theta_fc - theta_init

        df.ix[loc, "ro"] = get_ro(row.peff, theta_s, prev_theta)
        df.ix[loc, "dp"] = get_dp(row.peff, prev_theta, theta_fc, draintime)
        df.ix[loc, "ks"] = get_ks(prev_dr, taw, raw)
        # Note: For crop_evapotranspiration to be ET
        df.ix[loc, "etc"] = get_crop_evapotranspiration(row.et, kc, df.ix[loc, "ks"])
        df.ix[loc, "swb"] = (
            row.peff - CR + df.ix[loc, "etc"] + df.ix[loc, "dp"] + df.ix[loc, "ro"]
        )
        df.ix[loc, "dr"] = prev_dr + df.ix[loc, "swb"]
        # TODO: Verify that old fc_irt == mif.
        # inet: To denote no irrigation the value should be None not zero
        # This note need documentation.
        df.ix[loc, "inet"] = get_inet(df.ix[loc, "dr"], mif, raw, row.net)
        df.ix[loc, "dr_1"] = get_dr_1(df.ix[loc, "dr"], taw, df.ix[loc, "inet"])
        df.ix[loc, "theta"] = get_theta(
            theta_init, theta_s, theta_fc, df.ix[loc, "dr"], df.ix[loc, "inet"]
        )
        df.ix[loc, "advice"] = 1 if df.ix[loc, "dr"] >= raw else 0
    return df
