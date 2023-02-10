"""
 contains functions for calculation of the sun position in azimuth and elevation at
 any given location and time
 code is adapted from John Clark Craigs code published code as available on the website
 https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777
"""

import math
import numpy as np
from pandas import DataFrame, date_range

# Math typing shortcuts
rad, deg = math.radians, math.degrees
sin, cos, tan = math.sin, math.cos, math.tan
asin, atan2 = math.asin, math.atan2# Convert latitude and longitude to radians

def sunpos(latitude, longitude, timezone, year, month, day, hour, minute = 0, second = 0, refraction = False) ->tuple:
    """ calculates the sun position at given parameters and returns sun elevation and sun azimuth
   
    Returns:
        azimuth: azimuth angle in deg of the sun position (N=0deg, E=90deg, S=180deg, W=270deg)
        elevation: sun elevation above horizon in deg
    """
    rlat = rad(latitude)
    rlon = rad(longitude)# Decimal hour of the day at Greenwich
    greenwichtime = hour - timezone + minute / 60 + second / 3600
    # Days from J2000, accurate from 1901 to 2099
    daynum = (
            367 * year
            - 7 * (year + (month + 9) // 12) // 4
            + 275 * month // 9
            + day
            - 730531.5
            + greenwichtime / 24)
    # Mean longitude of the sun
    mean_long = daynum * 0.01720279239 + 4.894967873
    # Mean anomaly of the Sun
    mean_anom = daynum * 0.01720197034 + 6.240040768
    # Ecliptic longitude of the sun
    eclip_long = (
            mean_long
            + 0.03342305518 * sin(mean_anom)
            + 0.0003490658504 * sin(2 * mean_anom))
    # Obliquity of the ecliptic
    obliquity = 0.4090877234 - 0.000000006981317008 * daynum
    # Right ascension of the sun
    rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))
    # Declination of the sun
    decl = asin(sin(obliquity) * sin(eclip_long))
    # Local sidereal time
    sidereal = 4.894961213 + 6.300388099 * daynum + rlon
    # Hour angle of the sun
    hour_ang = sidereal - rasc
    # Local elevation of the sun
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))
    # Local azimuth of the sun
    azimuth = atan2(
            -cos(decl) * cos(rlat) * sin(hour_ang),
            sin(decl) - sin(rlat) * sin(elevation),)
    # Convert azimuth and elevation to degrees
    azimuth = into_range(deg(azimuth), 0, 360)
    elevation = into_range(deg(elevation), -180, 180)
    # Refraction correction (optional)
    if refraction:
        targ = rad((elevation + (10.3 / (elevation + 5.11))))
        elevation += (1.02 / tan(targ)) / 60# Return azimuth and elevation in degrees
    
    return (azimuth, elevation)

def into_range(x, range_min, range_max):
    shiftedx = x - range_min
    delta = range_max - range_min
    return (((shiftedx % delta) + delta) % delta) + range_min

def get_sun_positions(latitude, longitude, timezone, start_day, end_day) -> DataFrame:
    """ returns a DataFrame with hourly azimuth and elevation of the sun within given time range """

    sun_positions = DataFrame({"timestamp" : date_range(start=start_day, end=end_day, freq='H')})
    
    sun_az_el = np.array([ sunpos(latitude, longitude, timezone, dt.year, dt.month, dt.day, dt.hour) for dt in sun_positions["timestamp"] ])

    sun_az_el = sun_az_el.transpose()
    sun_positions["sun_az"] = sun_az_el[0]     
    sun_positions["sun_el"] = sun_az_el[1] 

    return sun_positions