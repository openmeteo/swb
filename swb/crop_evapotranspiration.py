import datetime as dt
from collections import namedtuple

import numpy as np

KcStage = namedtuple("KcStage", ("ndays", "kc_end"))


def calculate_crop_evapotranspiration(
    *, timeseries, planting_date, kc_offseason, kc_plantingdate, kc_stages
):
    model = CropEvapotranspiration(
        timeseries=timeseries,
        planting_date=planting_date,
        kc_offseason=kc_offseason,
        kc_plantingdate=kc_plantingdate,
        kc_stages=kc_stages,
    )
    model.calculate()


class CropEvapotranspiration(object):
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def calculate(self):
        self.timeseries["kc"] = self.kc_offseason
        prev_kc = self.kc_plantingdate
        days_done = 0
        for stage in self.kc_stages:
            self._calculate_stage(stage, prev_kc, days_done)
            days_done += stage.ndays
            prev_kc = stage.kc_end
        self.timeseries["crop_evapotranspiration"] = (
            self.timeseries["ref_evapotranspiration"] * self.timeseries["kc"]
        )

    def _calculate_stage(self, stage, kc_start, days_done):
        start_date = self.planting_date + dt.timedelta(days=days_done)
        end_date = self.planting_date + dt.timedelta(days=days_done + stage.ndays - 1)
        start = self._date_to_timestamp(start_date)
        end = self._date_to_timestamp(end_date)
        kcs = np.linspace(kc_start, stage.kc_end, num=stage.ndays + 1)[1:]
        period_length = len(self.timeseries.loc[start:end, "kc"])
        kcs = kcs[:period_length]
        self.timeseries.loc[start:end, "kc"] = kcs

    def _date_to_timestamp(self, date):
        try:
            time = self.timeseries.index[0].time()
        except IndexError:
            time = dt.time(0, 0)
        return dt.datetime.combine(date, time)
