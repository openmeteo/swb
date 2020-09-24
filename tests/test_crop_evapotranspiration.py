import datetime as dt
from unittest import TestCase

import numpy as np
import pandas as pd

from swb import KcStage, calculate_crop_evapotranspiration


class CalculateCropEvapotranspirationTestMixin:
    """Functional testing of calculate_crop_evapotranspiration().

    We use the example of FAO56 (Box 15, Figure 36, Example 28, pp. 130-133) for
    testing. We use 10 additional days before planting in order to test kc_offseason.

    Start of time series: 1974-05-13
    Planting date: 1974-05-23
    Total crop lifetime: 100 days (1974-05-23 to 1974-08-30)
    """

    def setUp(self):
        self._prepare_timeseries()
        calculate_crop_evapotranspiration(
            timeseries=self.timeseries,
            planting_date=dt.date(1974, 5, 23),
            kc_offseason=0.1,
            kc_plantingdate=0.15,
            kc_stages=(
                KcStage(25, 0.15),
                KcStage(25, 1.19),
                KcStage(30, 1.19),
                KcStage(20, 0.35),
            ),
        )

    def _prepare_timeseries(self):
        self.timeseries = pd.DataFrame(
            data={"ref_evapotranspiration": np.full(110, 3.14)},
            index=pd.date_range(self._get_date("1974-05-13"), periods=110),
        )

    def _get_date(self, datestr):
        return datestr

    def test_kc_start(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-05-13")]["kc"], 0.1, places=2
        )

    def test_kc_end_before_planting(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-05-22")]["kc"], 0.1, places=2
        )

    def test_kc_start_of_init(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-05-23")]["kc"], 0.15, places=2
        )

    def test_kc_end_of_init(self):
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-06-16")]["kc"], 0.15, places=2
        )

    def test_kc_june_21(self):
        # This result is indicated in a paragraph just below Figure 36. It's not clear
        # from that paragraph whether 0.36 should be on 20 June or on 21 June. Our code
        # produces this result on 21 June. Since we get the numbers for days 40, 70 and
        # 95 correctly (see other tests), we conclude 21 June is fine.
        self.assertAlmostEqual(
            self.timeseries.loc[self._get_date("1974-06-21")]["kc"], 0.36, places=2
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
            index=pd.date_range(self._get_date("1974-05-13"), periods=ndays),
        )
        calculate_crop_evapotranspiration(
            timeseries=partial_timeseries,
            planting_date=dt.date(1974, 5, 23),
            kc_offseason=0.1,
            kc_plantingdate=0.15,
            kc_stages=(
                KcStage(25, 0.15),
                KcStage(25, 1.19),
                KcStage(30, 1.19),
                KcStage(20, 0.35),
            ),
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
    """Test case for timeseries that end in a time different from 00:00."""

    def _get_date(self, datestr):
        return datestr + " 23:59"


class EmptyTimeseriesTestCase(TestCase):
    def setUp(self):
        self.timeseries = pd.DataFrame(data={"ref_evapotranspiration": []}, index=[])
        calculate_crop_evapotranspiration(
            timeseries=self.timeseries,
            planting_date=dt.date(1974, 5, 22),
            kc_offseason=0.1,
            kc_plantingdate=0.15,
            kc_stages=(
                KcStage(25, 0.15),
                KcStage(25, 1.19),
                KcStage(30, 1.19),
                KcStage(20, 0.35),
            ),
        )

    def test_result_is_empty(self):
        self.assertEqual(len(self.timeseries), 0)

    def test_result_has_kc(self):
        self.assertEqual(len(self.timeseries["kc"]), 0)

    def test_result_has_crop_evapotranspiration(self):
        self.assertEqual(len(self.timeseries["crop_evapotranspiration"]), 0)
