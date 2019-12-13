import datetime as dt
from unittest import TestCase

import numpy as np
import pandas as pd

from swb import calculate_crop_evapotranspiration


class CalculateCropEvapotranspirationTestMixin:
    """Functional testing of calculate_crop_evapotranspiration().

    We use the example of FAO56 (Box 15, Figure 36, Example 28, pp. 130-133) for
    testing. However we consider a planting date of one day earlier than what the
    example says, otherwise results don't agree. We also use 10 additional days before
    planting in order to test kc_unplanted.

    Start of time series: 1974-05-12
    Planting date: 1974-05-22
    Total crop lifetime: 100 days (1974-05-22 to 1974-08-29)
    """

    def setUp(self):
        self._prepare_timeseries()
        calculate_crop_evapotranspiration(
            timeseries=self.timeseries,
            planting_date=dt.date(1974, 5, 22),
            kc_unplanted=0.1,
            kc_ini=0.15,
            kc_mid=1.19,
            kc_end=0.35,
            init=25,
            dev=25,
            mid=30,
            late=20,
        )

    def _prepare_timeseries(self):
        self.timeseries = pd.DataFrame(
            data={"ref_evapotranspiration": np.full(110, 3.14)},
            index=pd.date_range(self._get_date("1974-05-12"), periods=110),
        )

    def _get_date(self, datestr):
        return datestr

    def test_kc_start(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-05-12")]["kc"], 0.1, places=2
        )

    def test_kc_end_before_planting(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-05-21")]["kc"], 0.1, places=2
        )

    def test_kc_start_of_init(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-05-22")]["kc"], 0.15, places=2
        )

    def test_kc_end_of_init(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-06-15")]["kc"], 0.15, places=2
        )

    def test_kc_june_20(self):
        # This result is indicated in a paragraph just below Figure 36
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-06-20")]["kc"], 0.36, places=2
        )

    def test_kc_on_day_40(self):
        # Example 28 p. 133
        self.assertAlmostEqual(self.timeseries.iloc[9 + 40]["kc"], 0.77, places=2)

    def test_kc_on_day_70(self):
        # Example 28 p. 133
        self.assertAlmostEqual(self.timeseries.iloc[9 + 70]["kc"], 1.19, places=2)

    def test_kc_on_day_95(self):
        # Example 28 p. 133
        self.assertAlmostEqual(self.timeseries.iloc[9 + 95]["kc"], 0.56, places=2)

    def test_kc_on_last_day(self):
        self.assertAlmostEqual(self.timeseries.iloc[9 + 100]["kc"], 0.35, places=2)

    def test_crop_evapotranspiration(self):
        # The hard part is to calculate Kc. The crop evapotranspiration is trivial.
        # We've specified a constant reference evapotranspiration of 3.14, and all we
        # need to do is check one day and verify that the multiplication with Kc has
        # been done correctly. We use day 40.
        self.assertAlmostEqual(
            self.timeseries.iloc[9 + 40]["crop_evapotranspiration"],
            3.14 * 0.774,
            places=2,
        )

    def test_partial_run_before_planting(self):
        self._test_partial_run(ndays=5)

    def test_partial_run_init(self):
        self._test_partial_run(ndays=30)

    def test_partial_run_dev(self):
        self._test_partial_run(ndays=50)

    def test_partial_run_mid(self):
        self._test_partial_run(ndays=80)

    def test_partial_run_late(self):
        self._test_partial_run(ndays=100)

    def _test_partial_run(self, ndays):
        """
        Test that when we run the model with a partial time series that has only "ndays"
        records the model runs properly until then. We do that by comparing the
        resulting crop evapotranspiration timeseries with the first ndays of the entire
        time series.
        """
        partial_timeseries = pd.DataFrame(
            data={"ref_evapotranspiration": np.full(ndays, 3.14)},
            index=pd.date_range(self._get_date("1974-05-12"), periods=ndays),
        )
        calculate_crop_evapotranspiration(
            timeseries=partial_timeseries,
            planting_date=dt.date(1974, 5, 22),
            kc_unplanted=0.1,
            kc_ini=0.15,
            kc_mid=1.19,
            kc_end=0.35,
            init=25,
            dev=25,
            mid=30,
            late=20,
        )
        pd.testing.assert_series_equal(
            partial_timeseries["crop_evapotranspiration"],
            self.timeseries["crop_evapotranspiration"][:ndays],
        )


class WithDateOnlyTimestampsTestCase(
    CalculateCropEvapotranspirationTestMixin, TestCase
):
    pass


class WithNonMidnightTimestampsTestCase(
    CalculateCropEvapotranspirationTestMixin, TestCase
):
    """Test case for timeseries that end in a time different from 00:00.
    """

    def _get_date(self, datestr):
        return datestr + " 23:59"


class EmptyTimeseriesTestCase(TestCase):
    def setUp(self):
        self.timeseries = pd.DataFrame(data={"ref_evapotranspiration": []}, index=[])
        calculate_crop_evapotranspiration(
            timeseries=self.timeseries,
            planting_date=dt.date(1974, 5, 22),
            kc_unplanted=0.1,
            kc_ini=0.15,
            kc_mid=1.19,
            kc_end=0.35,
            init=25,
            dev=25,
            mid=30,
            late=20,
        )

    def test_result_is_empty(self):
        self.assertEqual(len(self.timeseries), 0)

    def test_result_has_kc(self):
        self.assertEqual(len(self.timeseries["kc"]), 0)

    def test_result_has_crop_evapotranspiration(self):
        self.assertEqual(len(self.timeseries["crop_evapotranspiration"]), 0)
