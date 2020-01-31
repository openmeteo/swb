from unittest import TestCase

import pandas as pd

from swb import get_effective_precipitation


class GetEffectivePrecipitationTestCase(TestCase):
    def setUp(self):
        self._prepare_timeseries()
        get_effective_precipitation(timeseries=self.timeseries)

    def _prepare_timeseries(self):
        self.timeseries = pd.DataFrame(
            data={
                "ref_evapotranspiration": [1.6, 2.7, 3.8],
                "precipitation": [0.5, 0.6, 0.7],
            },
            index=pd.date_range("1974-05-12", periods=3),
        )

    expected_result = pd.DataFrame(
        data={
            "ref_evapotranspiration": [1.6, 2.7, 3.8],
            "precipitation": [0.5, 0.6, 0.7],
            "effective_precipitation": [0.4, 0.48, 0],
        },
        index=pd.date_range("1974-05-12", periods=3),
    )

    def test_get_effective_precipitation(self):
        pd.testing.assert_frame_equal(
            self.timeseries, self.expected_result, check_like=True
        )
