====================================================================
:func:`calculate_crop_evapotranspiration` --- Get |ET_c| from |ET_0|
====================================================================

.. |ET_0| replace:: ET\ :sub:`0`
.. |ET_c| replace:: ET\ :sub:`c`
.. |K_c| replace:: K\ :sub:`c`
.. |K_c_ini| replace:: K\ :sub:`c ini`
.. |K_c_mid| replace:: K\ :sub:`c mid`
.. |K_c_end| replace:: K\ :sub:`c end`
.. |K_c_unplanted| replace:: K\ :sub:`c unplanted`


Usage
=====

::

    from swb import calculate_crop_evapotranspiration

    calculate_crop_evapotranspiration(
       timeseries=a_pandas_dataframe,
       planting_date=dt.date(2019, 3, 21),
       kc_unplanted=0.3,
       kc_ini=0.7,
       kc_mid=1.05,
       kc_end=0.95,
       init=35,
       dev=45,
       mid=40,
       late=15,
   )

``timeseries`` is a pandas dataframe that contains a
``ref_evapotranspiration`` column with the reference evapotranspiration.
Two time series will be calculated and added to the dataframe: ``kc``
and ``crop_evapotranspiration``.  ``kc_unplanted`` is the |K_c| before
planting. ``kc_ini``, ``kc_mid`` and ``kc_end`` are the |K_c| in various
development stages of the plant.  ``init``, ``dev``, ``mid`` and
``late`` are the number of days of the development stages of the plant.
For details, see "Methodology" below.

Methodology
===========

The crop evapotranspiration equals the reference evapotranspiration
multiplied by the crop coefficient |K_c|. This crop coefficient is
different in different development stages of the plant. When it is young
and small, it transpires less water than when it is fully grown, and
as it gradually withers it transpires less and less. Therefore |K_c|
varies through the plant's development.

According to the methodology of :ref:`FAO56 <fao56>`, three values are
given for |K_c|: |K_c_ini|, |K_c_mid|, |K_c_end|. There are also four
development stages: initial, development, middle, and late.

In the initial stage, which lasts for ``init`` days, |K_c| equals
|K_c_ini|.

In the development stage, which lasts for ``dev`` days, |K_c| gradually
increases from |K_c_ini| to |K_c_mid|. This increase is linear.

In the middle stage, which lasts for ``mid`` days, |K_c| equals
|K_c_mid|.

In the late stage, which lasts for ``late`` days, |K_c| gradually
decreases from |K_c_mid| to |K_c_end|. The decrease is linear. On the
last day, |K_c| equals |K_c_end|.

For the period before planting, we need to know how much water is
evaporated by the soil; for this, we use |K_c_unplanted|. (Technically
this isn't "crop evapotranspiration" and the coefficient isn't |K_c|;
but in order to calculate depletion we need to know how much water has
evaporated from the soil and put this in the resulting time series.)


References
==========

.. _fao56:

R. G. Allen, L. S. Pereira, D. Raes, and M. Smith, Crop evapotranspiration -
Guidelines for computing crop water requirements, FAO Irrigation and drainage
paper no. 56, 1998.
