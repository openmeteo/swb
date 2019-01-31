# Copyright (C) 2013-2018  TEI of Epirus
# Copyright (C) 2018-2019  University of Ioannina
# GNU General Public License. See LICENSE
import pandas as pd

def _is_pdSeries(var):
    """
        Minor helper to validate if input 'var' is pandas Series instance
        Raise TypeError if not.
    """
    if not isinstance(var, pd.core.series.Series):
        raise TypeError("Input must be Pandas Series")
    return


def _validate_input_series(vars):
    """
        Validate input model meteo data
        1. Is pandas series
        2. Do all series have the same DateIndex
    """
    for var in vars:
        _is_pdSeries(var)
    a, b, c = vars
    assert [v for v in a.index] == [v for v in b.index] == [v for v in c.index]
    return
