=======
History
=======

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
