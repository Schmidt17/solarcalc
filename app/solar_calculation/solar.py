from numpy import cos, sin, deg2rad
import pandas as pd

from solar_calculation.sunpos import get_sun_positions
from solar_calculation.weather import get_sun_minutes


class SolarCell:
    def __init__(self, inclination, azimuth, pkpower_kW):
        """
            azimuth: sc facing angle in deg (facing N: 0deg, E: 90deg, S: 180deg, W: 270deg)
            inclination: sc inclination angle in deg
            pk_power_kW: peak power output of the solar cell in kW (kilo Watt)
        """
        self.check_inputs(pkpower_kW, azimuth, inclination)
        
        self.pkpower_kW = pkpower_kW
        self.azimuth = azimuth
        self.inclination = inclination

        # calculate and store values used for calculation of incidence factor
        self.lot_x = sin(deg2rad(azimuth)) * sin(deg2rad(inclination))
        self.lot_y = cos(deg2rad(azimuth)) * sin(deg2rad(inclination))
        self.lot_z = cos(deg2rad(inclination))

    def check_inputs(self, pkpower_kW: float, azimuth: float, inclination: float):
        # peak power
        if not pkpower_kW > 0.0:
            raise ValueError(f"SolarCell Error: peak power must be above 0.0kW, but is {pkpower_kW}.")        
        # azimuth
        if not 0 <= azimuth < 360:
            raise ValueError(f"SolarCell Error: solar cell azimuth must be in between 0deg to 360deg, but is {azimuth}.")        
        # inclination
        if not 0 <= inclination <= 90:
            raise ValueError(f"SolarCell Error: solar cell inclination must be in between 0deg to 90deg, but is {inclination}.")


def calc_sc_power(sun_az, sun_el, sun_minutes, sc: SolarCell) ->float:
    # check sun is up
    if sun_el <= 0:
        return 0
    # check sun shines
    if sun_minutes == 0:
        return 0
    # calculate effective incidence angle
    cos_gamma = sin(deg2rad(sun_az))*cos(deg2rad(sun_el)) * sc.lot_x + cos(deg2rad(sun_az))*cos(deg2rad(sun_el)) * sc.lot_y + sin(deg2rad(sun_el)) * sc.lot_z
    # calculate effective power output
    if cos_gamma <= 0:
        return 0
    else:
        return cos_gamma * sc.pkpower_kW * sun_minutes / 60

def get_solar_power_table(latitude, longitude, timezone, start_day, end_day, solar_cells: list) ->pd.DataFrame:
    """ calculates solar power for every hour within given time range and returns as DataFrame """

    sunpos_tbl = get_sun_positions(latitude= latitude,
                                      longitude = longitude,
                                      timezone = timezone,
                                      start_day=start_day,
                                      end_day=end_day)

    sunminutes = get_sun_minutes(start_day=start_day,
                                    end_day=end_day)

    power_tbl = sunpos_tbl.merge(sunminutes)

    for i, sc in enumerate(solar_cells):
        power_tbl[f"sc{i+1}"] = [ calc_sc_power(row["sun_az"], row["sun_el"], row["sun_minutes"], sc) for i, row in power_tbl.iterrows()   ]

    return power_tbl


