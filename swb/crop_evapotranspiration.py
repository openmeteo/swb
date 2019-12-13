import datetime as dt

import numpy as np


def calculate_crop_evapotranspiration(**kwargs):
    model = CropEvapotranspiration(**kwargs)
    model.calculate()


class CropEvapotranspiration(object):
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def calculate(self):
        self.timeseries["kc"] = 0
        self._calculate_kc_for_unplanted_stage()
        self._calculate_kc_for_init_stage()
        self._calculate_kc_for_dev_stage()
        self._calculate_kc_for_mid_stage()
        self._calculate_kc_for_late_stage()
        self.timeseries["crop_evapotranspiration"] = (
            self.timeseries["ref_evapotranspiration"] * self.timeseries["kc"]
        )

    def _date_to_timestamp(self, date):
        try:
            time = self.timeseries.index[0].time()
        except IndexError:
            time = dt.time(0, 0)
        return dt.datetime.combine(date, time)

    def _calculate_kc_for_unplanted_stage(self):
        end = self._date_to_timestamp(self.planting_date - dt.timedelta(days=1))
        self.timeseries.loc[:end, "kc"] = self.kc_unplanted

    def _calculate_kc_for_init_stage(self):
        start = self._date_to_timestamp(self.planting_date)
        end = start + dt.timedelta(days=self.init - 1)
        self.timeseries.loc[start:end, "kc"] = self.kc_ini

    def _calculate_kc_for_dev_stage(self):
        start = self._date_to_timestamp(
            self.planting_date + dt.timedelta(days=self.init)
        )
        end = start + dt.timedelta(days=self.dev - 1)
        dev_kcs = np.linspace(self.kc_ini, self.kc_mid, num=self.dev + 1)[1:]
        period_length = len(self.timeseries.loc[start:end, "kc"])
        dev_kcs = dev_kcs[:period_length]
        self.timeseries.loc[start:end, "kc"] = dev_kcs

    def _calculate_kc_for_mid_stage(self):
        start = self._date_to_timestamp(
            self.planting_date + dt.timedelta(days=self.init + self.dev)
        )
        end = start + dt.timedelta(days=self.mid - 1)
        self.timeseries.loc[start:end, "kc"] = self.kc_mid

    def _calculate_kc_for_late_stage(self):
        start = self._date_to_timestamp(
            self.planting_date + dt.timedelta(days=self.init + self.dev + self.mid)
        )
        end = start + dt.timedelta(days=self.late - 1)
        late_kcs = np.linspace(self.kc_mid, self.kc_end, num=self.late + 1)[1:]
        period_length = len(self.timeseries.loc[start:, "kc"])
        late_kcs = late_kcs[:period_length]
        self.timeseries.loc[start:end, "kc"] = late_kcs
