=======
History
=======

5.0.1 (2024-04-14)
------------------

- ``calculate_crop_evapotranspiration()`` now works with aware (as well
  as with naive) time series.

5.0.0 (2021-08-13)
------------------

- ``mif`` has been renamed to ``refill_factor``.

4.0.0 (2021-05-14)
------------------

- ``actual_net_irrigation`` cannot be ``True`` any more; instead, it can
  have the value "model" (same as what ``True`` was) or "fc" (new
  functionality).
- There is now an additional output column, ``assumed_net_irrigation``,
  useful when ``actual_net_irrigation`` is "model" or "fc".

3.0.0 (2020-09-24)
------------------

- ``calculate_crop_evapotranspiration()`` argument ``kc_initial`` has been
  renamed to ``kc_plantingdate``.

2.0.0 (2020-08-06)
------------------

- Only Python>=3.6 is supported.
- Specifying Kc for ``calculate_crop_evapotranspiration()`` has changed;
  it's now not only three values (Kc_init, Kc_mid, Kc_late), but an
  unlimited number of (number-of-days-in-stage, Kc-at-end-of-stage)
  pairs.

1.0.2 (2020-04-08)
------------------

- Fixed an issue when there was (unreasonably) large irrigation.

1.0.1 (2020-04-03)
------------------

- Added the constraint Dr ≤ TAW.

1.0.0 (2020-01-07)
------------------

- Added simple model to get effective precipitation from total
  precipitation.

0.3.3 (2019-12-13)
------------------

- Fixed crash when calculate_crop_evapotranspiration received a time
  series whose timestamps did not end in 00:00.

0.3.2 (2019-05-06)
------------------

- Fixed crop evapotranspiration model, which could only run for the
  entire period from planting to harvest; now it can run for part of the
  period.

0.3.1 (2019-03-27)
------------------

- Changed the way deep percolation is calculated; now uses ``theta -
  theta_fc`` rather than ``theta_s - theta_fc``.

0.3.0 (2019-03-26)
------------------

- Fixed swb errors with deep percolation.

0.2.0 (2019-03-23)
------------------

- Added model for calculation of crop evapotranspiration from reference
  evapotranspiration.

0.1.0 (2019-03-14)
------------------

- Initial release
