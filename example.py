import numpy as np
import pandas as pd
from swb import calculate_soil_water

## Fake data
_DATEINDEX =  pd.date_range(
    start='1/1/2018', end='12/31/2018',
    freq='D' # default / daily
)
_LEN = len(_DATEINDEX)

def generate_data(len, neg=False):
    # Minor helper
    if neg:
        return np.random.randn(len)
    return np.random.rand(len)

## Run model
MODEL_PARAMETERS = {
    'theta_s': 0.425,
    'theta_fc': 0.287,
    'theta_wp': 0.140,
    'rd': 0.5,
    'zr_factor': 0.3,
    'kc': 0.7,
    'p': 0.5,
    'draintime': 1.3,
    'effective_precipitation': pd.Series(
            data=generate_data(_LEN, False),
            index=_DATEINDEX,
            name='effective_precipitation'
    ),
    'crop_evapotranspiration': pd.Series(
            data=generate_data(_LEN, True),
            index=_DATEINDEX,
            name='crop_evapotranspiration'
    ),
    'net_irrigation': pd.Series(
            data=generate_data(_LEN, False),
            index=_DATEINDEX,
            name='net_irrigation'
    ),
    'theta_init': 0.453,
    'mif': 2.1, # The Malamos irrigation fraction !!!
}


def main():
    swb = calculate_soil_water(**MODEL_PARAMETERS)
    print(swb.head())
    return;

if __name__ == '__main__':
    main()
