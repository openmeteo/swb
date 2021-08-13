from unittest import TestCase

import numpy as np
import pandas as pd

from swb import SoilWaterBalance, calculate_soil_water


class SimpleMethodsTestCase(TestCase):
    def setUp(self):
        self.swb = SoilWaterBalance(
            theta_s=0.425,
            theta_fc=0.287,
            theta_wp=0.14,
            zr=0.5,
            zr_factor=1000,
            p=0.5,
            draintime=16.2,
            timeseries=None,
            theta_init=None,
            refill_factor=None,
        )

    def test_taw(self):
        self.assertAlmostEqual(self.swb.taw, 73.5)

    def test_raw(self):
        self.assertAlmostEqual(self.swb.raw, 36.75)

    def test_dr_from_theta(self):
        self.assertAlmostEqual(self.swb.dr_from_theta(0.277326), 4.837, places=3)

    def test_theta_from_dr(self):
        self.assertAlmostEqual(self.swb.theta_from_dr(4.837), 0.277, places=3)

    def test_ks(self):
        self.assertAlmostEqual(self.swb.ks(37.746), 0.973, places=3)

    def test_ks_when_above_threshold(self):
        self.assertAlmostEqual(self.swb.ks(30), 1)

    def test_dp(self):
        self.assertAlmostEqual(self.swb.dp(0.311, 0), 0.741, places=3)

    def test_dp_zero(self):
        self.assertEqual(self.swb.dp(0.186, 0), 0)

    def test_ro_at_saturation(self):
        # When we are already saturated (0.425), all precipitation (15 mm) runs off
        self.assertAlmostEqual(self.swb.ro(15, 0.425), 15)

    def test_ro_zero(self):
        # When the soil is practically dry and 2 mm falls, nothing runs off
        self.assertEqual(self.swb.ro(2, 0.14), 0)


class ModelTestCase(TestCase):
    @classmethod
    def setUpData(cls):
        data = {
            "effective_precipitation": [0, 0, 4, 0],
            "actual_net_irrigation": [3000, 0, 0, 0],
            "crop_evapotranspiration": [49, 350, 3.5, 49],
        }
        cls.df = pd.DataFrame(data, index=pd.date_range("2018-03-15", periods=4))

    @classmethod
    def setUpClass(cls):
        cls.setUpData()
        calculate_soil_water(
            theta_s=0.5,
            theta_fc=0.4,
            theta_wp=0.1,
            zr=0.95,
            zr_factor=1000,
            p=0.5,
            draintime=28.6,
            timeseries=cls.df,
            theta_init=0.4,
            refill_factor=0.5,
        )

    def test_dr(self):
        np.testing.assert_almost_equal(
            self.df["dr"], [-2951.0, 258.3, 255.0, 265.3], decimal=1
        )

    def test_theta(self):
        np.testing.assert_almost_equal(
            self.df["theta"], [3.506, 0.128, 0.132, 0.121], decimal=3
        )

    def test_ks(self):
        np.testing.assert_almost_equal(self.df["ks"], [1, 1, 0.187, 0.211], decimal=3)

    def test_recommended_net_irrigation(self):
        np.testing.assert_almost_equal(
            self.df["recommended_net_irrigation"], [0, 129.2, 127.5, 132.7], decimal=1
        )

    def test_assumed_net_irrigation(self):
        np.testing.assert_almost_equal(
            self.df["assumed_net_irrigation"], [3000, 0, 0, 0], decimal=3
        )


class AutoApplyIrrigationTestCase(ModelTestCase):
    @classmethod
    def setUpData(cls):
        data = {
            "effective_precipitation": [0, 0, 4, 0],
            "actual_net_irrigation": ["model", "model", "model", "model"],
            "crop_evapotranspiration": [49, 350, 3.5, 49],
        }
        cls.df = pd.DataFrame(data, index=pd.date_range("2018-03-15", periods=4))

    def test_dr(self):
        np.testing.assert_almost_equal(
            self.df["dr"], [49, 199.5, 98.8, 73.9], decimal=1
        )

    def test_theta(self):
        np.testing.assert_almost_equal(
            self.df["theta"], [0.348, 0.190, 0.296, 0.322], decimal=3
        )

    def test_ks(self):
        np.testing.assert_almost_equal(self.df["ks"], [1, 1, 0.600, 1], decimal=3)

    def test_recommended_net_irrigation(self):
        np.testing.assert_almost_equal(
            self.df["recommended_net_irrigation"], [0, 199.5, 98.8, 73.9], decimal=1
        )

    def test_assumed_net_irrigation(self):
        np.testing.assert_almost_equal(
            self.df["assumed_net_irrigation"], [0, 199.5, 98.8, 73.9], decimal=1
        )


class ModelRunWithDrOutsideLimitsTestCase(TestCase):
    """Test FAO56 eq. 86 p. 170."""

    def setUp(self):
        data = {
            "effective_precipitation": [0, 80],
            "actual_net_irrigation": [0, 0],
            "crop_evapotranspiration": [50, 0.1],
        }
        self.df = pd.DataFrame(data, index=pd.date_range("2016-03-10", periods=2))
        result = calculate_soil_water(
            theta_s=0.425,
            theta_fc=0.287,
            theta_wp=0.14,
            zr=0.5,
            zr_factor=1000,
            p=0.5,
            draintime=16.3,
            timeseries=self.df,
            theta_init=0.15,
            refill_factor=1.0,
        )
        self.taw = result["taw"]

    def test_dr(self):
        np.testing.assert_almost_equal(self.df["dr"], [self.taw, -6.101], decimal=3)


class DpTestCase(TestCase):
    def setUp(self):
        self.swb = SoilWaterBalance(
            theta_s=0.425,
            theta_fc=0.287,
            theta_wp=0.14,
            zr=0.5,
            zr_factor=1000,
            p=0.5,
            draintime=16.3,
            timeseries=None,
            theta_init=0.15,
            refill_factor=1.0,
        )

    def test_dp_when_theta_less_than_theta_s(self):
        self.assertAlmostEqual(self.swb.dp(0.4, 20.0), 4.69325153)

    def test_dp_when_theta_more_than_theta_s(self):
        self.assertAlmostEqual(self.swb.dp(0.5, 20.0), 5.46012270)
