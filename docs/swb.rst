==================================================================
:func:`calculate_soil_water` --- Calculation of soil water balance
==================================================================

.. |CR_i| replace:: CR\ :sub:`i`
.. |D_r| replace:: D\ :sub:`r`
.. |D_r1| replace:: D\ :sub:`r,1`
.. |D_ri| replace:: D\ :sub:`r,i`
.. |D_ri-1| replace:: D\ :sub:`r,i-1`
.. |DP_i| replace:: DP\ :sub:`i`
.. |ET_0| replace:: ET\ :sub:`0`
.. |ET_ci| replace:: ET\ :sub:`c,i`
.. |IR_ni| replace:: IR\ :sub:`n,i`
.. |K_s| replace:: K\ :sub:`s`
.. |K_c| replace:: K\ :sub:`c`
.. |m3| replace:: m\ :sup:`3`
.. |P_i| replace:: P\ :sub:`i`
.. |RO_i| replace:: RO\ :sub:`i`
.. |Z_r| replace:: Z\ :sub:`r`
.. |θ_fc| replace:: θ\ :sub:`fc`
.. |θ_wp| replace:: θ\ :sub:`wp`
.. |θ_s| replace:: θ\ :sub:`s`
.. |θ_i-1| replace:: θ\ :sub:`i-1`
.. |p_eff| replace:: p\ :sub:`eff`


Usage
=====

::

    from swb import calculate_soil_water

    results = calculate_soil_water(
       theta_s=0.425,
       theta_fc=0.287,
       theta_wp=0.14,
       zr=0.5,
       zr_factor=1000,
       p=0.5,
       draintime=2.2,
       timeseries=a_pandas_dataframe,
       theta_init=0.19,
       mif=0.5,
   )

See the reference section below for what all this means.

Methodology
===========

Introduction
------------

This module provides the :func:`calculate_soil_water` function, which
calculates soil water content.

The soil is, so to speak, full of water when it is at field capacity and
empty when it is at wilting point.

The **field capacity** is below saturation point.  When the soil is
saturated, any excess water runs off immediately; when it is between
field capacity and saturation, the soil drains downward, usually in 2-3
days; when the soil is at or below field capacity, water is lost only
through evapotranspiration.  The field capacity is roughly the amount of
water that the soil can keep indefinitely without percolation.  It is a
property of the soil.

The **wilting point** (also called "permanent wilting point") is the
amount of water needed for plants to not wilt. It is a property of the
soil.

We are interested only in the topmost part of the soil, which is called
the **root zone**. It is the part of the soil that contains plant roots.
The depth of the root zone is a property of the crop.

The **depletion** (more precisely the "root zone depletion") is the
amount of water missing from the soil (more precisely the root zone).
When the soil is "full" (at field capacity) the depletion is zero. When
it is "half-empty", the depletion is the amount of water that would be
needed to "fill it up"; that is, the amount of water that is needed to
reach field capacity. The depletion is normally measured in mm.

This is the relation between depletion |D_r| and water content θ:
 
   |D_r| = (|θ_fc| - θ) |Z_r|

(:ref:`FAO56 <fao56>`, p. 170 eq. 87)

where:

 * θ is the water content. It is a proper number (|m3|/|m3|).
 * |θ_fc| is the water content at field capacity.
 * |Z_r| is the root zone depth.

Often |Z_r| is in meters and depletion in mm, so the equation becomes

   |D_r| = (|θ_fc| - θ) × |Z_r| × 1000

(In the rest of this text, we call 1000 the "root depth factor" or
`zr_factor`).

As we said, the soil is "full" at field capacity and "empty" at wilting
point.  The difference between these two is the **total available
water** or TAW. In other words, if the soil was a reservoir, the TAW
would be its capacity. The TAW is normally measured in mm.

   TAW = (|θ_fc| - |θ_wp|) × |Z_r| × `zr_factor`

(:ref:`FAO56 <fao56>`, p. 162 eq. 82)

Since saturation is above field capacity, the soil can be "overfull", so
to speak, in which case depletion is negative. The **drain time** is the
time the soil needs to go from saturation (|θ_s|) to field capacity
(|θ_fc|) solely because of downward movement (percolation) (i.e. if
evapotranspiration is zero).

Although plants can theoretically survive whenever the water content is
above wilting point, there's a threshold below which they are stressed.
This is different from crop to crop. The difference between field
capacity and this threshold is the **readily available water**:

   RAW = p TAW

(:ref:`FAO56 <fao56>`, p. 162 eq. 83)

The factor *p*, called "soil water depletion fraction for no stress", is
a property of the crop.

When the water content is above the threshold (|D_r| < RAW), the crop
evapotranspiration is |K_c| × |ET_0|, where |ET_0| the reference
evapotranspiration and |K_c| the crop coefficient. When the water
content is below the threshold (|D_r| > RAW), the crop is stressed and
decreases the amount of evapotranspiration to |K_s| × |K_c| × |ET_0|
where |K_s| is the **water stress coefficient**:

   |K_s| = (TAW - |D_r|) / (TAW - RAW) = (TAW - |D_r|) / ((1-p) TAW)

(:ref:`FAO56 <fao56>`, p. 169 eq. 84)

When the water content reaches the threshold (i.e. when |D_r| reaches
RAW), we need to irrigate. Normally the amount of water we irrigate with
is RAW. But sometimes we prefer to throw in a fraction of that amount.
This will result in more frequent irrigations thereafter and is
beneficial in some cases. :ref:`TEIEP (2014, p. 92) <teiep2014>`
confusingly calls this fraction the "irrigation optimizer", but we are
going to call it the **malamos irrigation fraction** or mif.

Calculation of depletion
------------------------
   
The basis for the calculation is this formula:

    |D_ri| = |D_ri-1| - (|P_i| - |RO_i|) - |IR_ni| - |CR_i| + |ET_ci| + |DP_i|

(:ref:`FAO56 <fao56>`, p. 170 eq. 85)

where:

 * *i* is the current time period (i.e. the current day).
 * |D_ri| is the root zone depletion at the end of time period *i*.
 * |P_i| is the effective precipitation (see below).
 * |RO_i| is the runoff (see below).
 * |IR_ni| is the net irrigation depth (see below).
 * |CR_i| is the capillary rise.
 * |ET_ci| is the crop evapotranspiration.
 * |DP_i| is the water loss through deep percolation.

|CR_i| is ignored and considered zero.

The evapotranspiration |ET_ci| is the reference evapotranspiration
multiplied by the crop coefficient |K_c|.

The **runoff** is the amount of water that exceeds saturation after
heavy rainfall:

  |RO_i| = |P_i| + (|θ_i-1| - |θ_s|) |Z_r| when larger than zero

(:ref:`Malamos et al., 2016 <malamos2016>`, eq. 5)

The **effective precipitation** is the precipitation that actually falls
on the soil. It is essentially the total precipitation minus the amount
that is held by the leaves.  :mod:`swb` does not contain any model
that converts total precipitation to effective precipitation; you need
to make this conversion and call :func:`calculate_soil_water` with the
effective precipitation. (A trivial model that you can use is multiply
total precipitation by a factor, |p_eff|, usually 0.8; it's quite crude,
but it's better than nothing.)

The **net irrigation depth** is the amount of water that
reaches the soil during irrigation. It is the total amount of water
consumed for irrigation minus losses. :mod:`swb` does not convert
between total and net irrigation; it accepts net irrigation as input
(and includes net irrigation in its output).

The **deep percolation** is zero if we are at or below field capacity.
If we are above field capacity (|θ_fc| < θ < |θ_s|) it is this:

   |DP_i| = (|θ_s| - |θ_fc|) * |Z_r| / `draintime`

(i.e. if we need `draintime` days to go from |θ_s| to |θ_fc|, then each
day we lose 1/`draintime` of that amount)


Reference
=========

.. function:: calculate_soil_water(**kwargs)

   Calculates soil water balance. Example::

       results = calculate_soil_water(
           theta_s=0.425,
           theta_fc=0.287,
           theta_wp=0.14,
           zr=0.5,
           zr_factor=1000,
           p=0.5,
           draintime=2.2,
           timeseries=a_pandas_dataframe,
           theta_init=0.19,
           mif=0.5,
       )
       
   :param float theta_s: Water content at saturation.
   :param float theta_fc: Water content at field capacity.
   :param float theta_wp: Water content at wilting point.
   :param float zr: The root depth.
   :param float zr_factor:
      If the root depth is in a different unit than the water depth variables
      (such as evapotranspiration, precipitation, irrigation and depletion)
      :attr:`zr_factor` is used to convert it.  If the root depth is in metres
      and the water depth variables are in mm, specify ``zr_factor=1000``.

   :param float p: The soil water depletion fraction for no stress.

   :param float draintime:
      The time, in days, needed for the soil to drain from saturation to
      field capacity.

   :param dataframe timeseries:
      A pandas dataframe indexed by date, containing two or three
      columns with input time series. The dataframe and its time series
      must be continuous and have no missing values. The columns are
      "crop_evapotranspiration", "effective_precipitation" and
      "actual_net_irrigation". All time series should be in mm; more
      precisely, in the same unit as the resulting depletion.

      The "crop_evapotranspiration" is the potential crop
      evapotranspiration (that is, the reference evapotranspiration
      multiplied by the crop coefficient |K_c|).

      The "actual_net_irrigation" is the applied net irrigation (that
      is, the total applied irrigation multiplied by the irrigation
      efficiency).

      If in a day it is known that we irrigated but not how much,
      "applied_net_irrigation" may simply be the boolean ``True`` for
      that day. In this case, it is assumed that we irrigated with the
      recommended amount that was calculated by the model.

   :param float theta_init:
      The initial water content (that is, the water content at the first date
      of the time series).

   :param float mif: The Malamos irrigation fraction.

   :rtype: dict

   :return:
      A dictionary with the results. It contains the following
      items:

      :raw: The readily available water.
      :taw: The total available water.
      :timeseries:
         The original dataframe with additional columns added, namely
         ``dr`` for depletion, ``theta`` for soil moisture, ``ks`` for
         the water stress coefficient, and
         ``recommended_net_irrigation`` for the calculated recommended
         net irrigation.  The original dataframe is changed in place (so
         the caller doesn't really need it returned), but the original
         columns and index are untouched.

References
==========

.. _fao56:

R. G. Allen, L. S. Pereira, D. Raes, and M. Smith, Crop evapotranspiration -
Guidelines for computing crop water requirements, FAO Irrigation and drainage
paper no. 56, 1998.

.. _malamos2016:

N. Malamos, I. L. Tsirogiannis, and A. Christofides, Modelling
irrigation management services: the IRMA_SYS case, International
Journal of Sustainable Agricultural Management and Informatics, 2
(1), 1–18, 2016.

.. _teiep2014:

TEIEP (Technological Educational Institute of Epirus), Deliverable
5.3.1: Detailed plan regarding the information system setup, for project
Development of an Irrigation Information System for the plain of Arta
(IRMA_SYS Arta), 2014. Available at
https://irma.irrigation-management.eu/deliverables/Del531_DPIRMASYS.pdf
