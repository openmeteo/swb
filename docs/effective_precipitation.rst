==========================================================
:func:`get_effective_precipitation` --- Get |P_eff| from P
==========================================================

.. |P_eff| replace:: P\ :sub:`eff`

Usage
=====

::

    from swb import get_effective_precipitation

    get_effective_precipitation(timeseries)

``timeseries`` is a pandas dataframe in daily step that contains a
``precipitation`` column and a ``ref_evapotranspiration`` (reference
evapotranspiration) column. The function adds an
``effective_precipitation`` column to the data frame. This is calculated
with a simple model: The effective precipitation is 0.8 times the
precipitation, unless the daily precipitation is less than a fifth of
the reference evapotranspiration, in which case the effective
precipitation is zero.
