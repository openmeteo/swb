import numpy as np


def get_effective_precipitation(timeseries):
    e = timeseries["ref_evapotranspiration"]
    p = timeseries["precipitation"]
    timeseries["effective_precipitation"] = np.where(p >= 0.2 * e, p * 0.8, 0.0)
