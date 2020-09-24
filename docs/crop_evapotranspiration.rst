====================================================================
:func:`calculate_crop_evapotranspiration` --- Get |ET_c| from |ET_0|
====================================================================

.. |ET_0| replace:: ET\ :sub:`0`
.. |ET_c| replace:: ET\ :sub:`c`
.. |K_c| replace:: K\ :sub:`c`
.. |K_c_ini| replace:: K\ :sub:`c ini`
.. |K_c_mid| replace:: K\ :sub:`c mid`
.. |K_c_end| replace:: K\ :sub:`c end`
.. |K_c_offseason| replace:: K\ :sub:`c os`


Usage
=====

::

    from swb import KcStage, calculate_crop_evapotranspiration

    calculate_crop_evapotranspiration(
       timeseries=a_pandas_dataframe,
       planting_date=dt.date(2019, 3, 21),
       kc_offseason=0.3,
       kc_plantingdate=0.7,
       kc_stages=(
          KcStage(35, 0.7),
          KcStage(45, 1.05),
          KcStage(40, 1.05),
          KcStage(15, 0.95),
       ),
   )

``timeseries`` is a pandas dataframe that contains a
``ref_evapotranspiration`` column with the reference evapotranspiration.
Two time series will be calculated and added to the dataframe: ``kc``
and ``crop_evapotranspiration``.  ``kc_stages`` specifies the |K_c|
stages, that is, a sequence of (number of days in stage, |K_c| at end of
stage) pairs. ``KcStage`` is a named tuple whose items are ``ndays`` and
``kc_end``. The planting_date corresponds to the beginning (day 1) of
the first stage. At each stage, we do linear interpolation between the
|K_c| at the end of the stage and the |K_c| at the end of the previous
stage (or ``kc_plantingdate`` if there's no previous stage).

This is a generalization of the methodology of :ref:`FAO56 <fao56>`,
where three values are given for |K_c| (|K_c_ini|, |K_c_mid|,
|K_c_end|), and there are four development stages: initial, development,
middle, and late. The example above is equivalent to |K_c_ini| = 0.7,
|K_c_mid| = 1.05, |K_c_end| = 0.95, initial = 35 days,  development = 45
days, middle = 40 days, late = 15 days. It also assumes a
|K_c_offseason| (off-season) of 0.3, i.e. how much water is evaporated by the
soil before planting. (Technically this isn't "crop evapotranspiration" and
the coefficient isn't |K_c|; but in order to calculate depletion we need
to know how much water has evaporated from the soil and put this in the
resulting time series.)


References
==========

.. _fao56:

R. G. Allen, L. S. Pereira, D. Raes, and M. Smith, Crop evapotranspiration -
Guidelines for computing crop water requirements, FAO Irrigation and drainage
paper no. 56, 1998.
