from unittest import TestCase

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
            mif=None,
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
        self.assertAlmostEqual(self.swb.dp(0.311), 4.259, places=3)

    def test_dp_zero(self):
        self.assertEqual(self.swb.dp(0.186), 0)

    def test_ro_at_saturation(self):
        # When we are already saturated (0.425), all precipitation (15 mm) runs off
        self.assertAlmostEqual(self.swb.ro(15, 0.425), 15)

    def test_ro_zero(self):
        # When the soil is practically dry and 2 mm falls, nothing runs off
        self.assertEqual(self.swb.ro(2, 0.14), 0)


class ModelRunWithActualNetIrrigationTestCase(TestCase):
    def setUp(self):
        data = {
            "effective_precipitation": [0, 4.8],
            "actual_net_irrigation": [0, 0],
            "crop_evapotranspiration": [3.871, 3.990],
        }
        self.df = pd.DataFrame(data, index=pd.date_range("2019-03-07", periods=2))
        calculate_soil_water(
            theta_s=0.425,
            theta_fc=0.287,
            theta_wp=0.14,
            zr=0.5,
            zr_factor=1000,
            p=0.5,
            draintime=16.2,
            timeseries=self.df,
            theta_init=0.252784,
            mif=None,
        )

    def test_dr1(self):
        self.assertAlmostEqual(self.df.iloc[0]["dr"], 20.979, places=3)

    def test_dr2(self):
        self.assertAlmostEqual(self.df.iloc[1]["dr"], 20.169, places=3)

    def test_theta1(self):
        self.assertAlmostEqual(self.df.iloc[0]["theta"], 0.245, places=3)

    def test_theta2(self):
        self.assertAlmostEqual(self.df.iloc[1]["theta"], 0.247, places=3)

    def test_ks1(self):
        self.assertAlmostEqual(self.df.iloc[0]["ks"], 1)

    def test_ks2(self):
        self.assertAlmostEqual(self.df.iloc[1]["ks"], 1)

    def test_recommended_net_irrigation1(self):
        self.assertAlmostEqual(self.df.iloc[0]["recommended_net_irrigation"], 0)

    def test_recommended_net_irrigation2(self):
        self.assertAlmostEqual(self.df.iloc[1]["recommended_net_irrigation"], 0)


class ModelRunWithNonzeroKsTestCase(TestCase):
    def setUp(self):
        data = {
            "effective_precipitation": [0, 0],
            "actual_net_irrigation": [0, 0],
            "crop_evapotranspiration": [3.724, 3.906],
        }
        self.df = pd.DataFrame(data, index=pd.date_range("2019-08-18", periods=2))
        calculate_soil_water(
            theta_s=0.425,
            theta_fc=0.287,
            theta_wp=0.14,
            zr=0.5,
            zr_factor=1000,
            p=0.5,
            draintime=16.2,
            timeseries=self.df,
            theta_init=0.218956,
            mif=1,
        )

    def test_dr1(self):
        self.assertAlmostEqual(self.df.iloc[0]["dr"], 37.746, places=3)

    def test_dr2(self):
        self.assertAlmostEqual(self.df.iloc[1]["dr"], 41.546, places=3)

    def test_theta1(self):
        self.assertAlmostEqual(self.df.iloc[0]["theta"], 0.212, places=3)

    def test_theta2(self):
        self.assertAlmostEqual(self.df.iloc[1]["theta"], 0.204, places=3)

    def test_ks1(self):
        self.assertAlmostEqual(self.df.iloc[0]["ks"], 1)

    def test_ks2(self):
        self.assertAlmostEqual(self.df.iloc[1]["ks"], 0.973, places=3)


class ModelRunWithAutoApplyIrrigationTestCase(TestCase):
    def setUp(self):
        data = {
            "effective_precipitation": [0, 0, 0],
            "actual_net_irrigation": [True, True, True],
            "crop_evapotranspiration": [3.647, 3.822, 3.885],
        }
        self.df = pd.DataFrame(data, index=pd.date_range("2019-03-07", periods=3))
        calculate_soil_water(
            theta_s=0.425,
            theta_fc=0.287,
            theta_wp=0.14,
            zr=0.5,
            zr_factor=1000,
            p=0.5,
            draintime=16.2,
            timeseries=self.df,
            theta_init=0.223646,
            mif=1.0,
        )

    def test_dr1(self):
        self.assertAlmostEqual(self.df.iloc[0]["dr"], 35.324, places=3)

    def test_dr2(self):
        self.assertAlmostEqual(self.df.iloc[1]["dr"], 0, places=3)

    def test_dr3(self):
        self.assertAlmostEqual(self.df.iloc[2]["dr"], 3.885, places=3)

    def test_theta1(self):
        self.assertAlmostEqual(self.df.iloc[0]["theta"], 0.216, places=3)

    def test_theta2(self):
        self.assertAlmostEqual(self.df.iloc[1]["theta"], 0.287, places=3)

    def test_theta3(self):
        self.assertAlmostEqual(self.df.iloc[2]["theta"], 0.279, places=3)

    def test_recommended_net_irrigation1(self):
        self.assertAlmostEqual(self.df.iloc[0]["recommended_net_irrigation"], 0)

    def test_recommended_net_irrigation2(self):
        self.assertAlmostEqual(
            self.df.iloc[1]["recommended_net_irrigation"], 39.146, places=3
        )

    def test_recommended_net_irrigation3(self):
        self.assertAlmostEqual(self.df.iloc[2]["recommended_net_irrigation"], 0)


class MifTestCase(TestCase):
    def setUp(self):
        data = {
            "effective_precipitation": [0, 0, 0],
            "actual_net_irrigation": [True, True, True],
            "crop_evapotranspiration": [3.647, 3.822, 3.885],
        }
        self.df = pd.DataFrame(data, index=pd.date_range("2019-03-07", periods=3))
        calculate_soil_water(
            theta_s=0.425,
            theta_fc=0.287,
            theta_wp=0.14,
            zr=0.5,
            zr_factor=1000,
            p=0.5,
            draintime=16.2,
            timeseries=self.df,
            theta_init=0.223646,
            mif=0.5,
        )

    def test_dr1(self):
        self.assertAlmostEqual(self.df.iloc[0]["dr"], 35.324, places=3)

    def test_dr2(self):
        self.assertAlmostEqual(self.df.iloc[1]["dr"], 19.573, places=3)

    def test_dr3(self):
        self.assertAlmostEqual(self.df.iloc[2]["dr"], 23.458, places=3)

    def test_recommended_net_irrigation1(self):
        self.assertAlmostEqual(self.df.iloc[0]["recommended_net_irrigation"], 0)

    def test_recommended_net_irrigation2(self):
        self.assertAlmostEqual(
            self.df.iloc[1]["recommended_net_irrigation"], 19.573, places=3
        )

    def test_recommended_net_irrigation3(self):
        self.assertAlmostEqual(self.df.iloc[2]["recommended_net_irrigation"], 0)
