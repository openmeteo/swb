=======
History
=======

0.3.2 (2019-05-06)
------------------

- Fix crop evapotranspiration model, which could only run for the entire
  period from planting to harvest; now it can run for part of the
  period.

0.3.1 (2019-03-27)
------------------

- Change the way deep percolation is calculated; use ``theta - theta_fc``
  rather than ``theta_s - theta_fc``.

0.3.0 (2019-03-26)
------------------

- Fixed swb errors with deep percolation

0.2.0 (2019-03-23)
------------------

- Added model for calculation of crop evapotranspiration from reference
  evapotranspiration

0.1.0 (2019-03-14)
------------------

- Initial release
