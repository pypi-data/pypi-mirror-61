__author__ = 'Dror Paz'
__createdOn__ = '2019/10/08'

import pytest
from datetime import datetime
from . import PE_Oudin


def test_pe_oudin():
    example_temp = [20, 25]  # Degrees celcius
    date = [datetime(2018, 1, 1), datetime(2018, 1, 1)]
    example_lat = 32  # Degrees (but can be set to radians)
    example_lat_unit = 'deg'  # Optional, and default. Can also be 'rad'
    example_out_units = 'mm/day'  # Optional, and default. Can also be 'mm/month' or 'mm/year'

    # Run program with single value
    pe = PE_Oudin.pe_oudin(example_temp[0], date[0], example_lat, example_lat_unit, example_out_units)
    assert pe == pytest.approx(1.948655)

    # Run program with multiple values
    pe = PE_Oudin.pe_oudin(example_temp, date, example_lat, example_lat_unit, example_out_units)
    assert pe == pytest.approx((1.948655, 2.338386))


def test_hourly_pe():
    example_temp = 20  # Degrees celcius
    time = datetime(2019, 1, 1, 12)
    example_lat = 32  # Degrees (but can be set to radians)
    example_out_units = 'mm/hour'  # Optional, and default. Can also be 'mm/month' or 'mm/year'
    pe = PE_Oudin.pe_oudin(temp=example_temp, time=time, lat=example_lat, out_units=example_out_units)
    expected = 0.22799268
    assert pe == pytest.approx(expected)
