import pandas as pd


def calculate_soil_water(
    *,
    theta_s,
    theta_fc,
    theta_wp,
    rd,
    zr_factor,
    kc,
    p,
    draintime,
    effective_precipitation,
    crop_evapotranspiration,
    net_irrigation,
    theta_init,
    mif
):
    pd  # I use this instead of "pass" to avoid a warning
