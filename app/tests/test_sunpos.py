import unittest
import solar_calculation.sunpos as sp


class Testsunpos(unittest.TestCase):

    def test_sunpos(self):
        # test data was generated with original version of 
        # https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777
        # and confirmed with data from:
        # https://gml.noaa.gov/grad/solcalc/
        sunpos_test_data = [{"latitude": 0.0, "longitude": 0.0, "timezone": 0,
                             "year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0, "second": 0, "refraction": True,
                             "elevation":  66.9598, "azimuth": 178.0573},
                            {"latitude": 0.0, "longitude": 0.0, "timezone": 0,
                             "year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0, "second": 0, "refraction": False,
                             "elevation":  66.9526, "azimuth": 178.0573},
                            {"latitude": 10.0, "longitude": 10.0, "timezone": 0,
                             "year": 2010, "month": 10, "day": 10, "hour": 10, "minute": 0, "second": 0, "refraction": True,
                             "elevation": 66.4117, "azimuth": 134.3108},
                            {"latitude": 10.0, "longitude": 10.0, "timezone": 0,
                             "year": 2010, "month": 10, "day": 10, "hour": 10, "minute": 0, "second": 0, "refraction": False,
                             "elevation": 66.4043, "azimuth": 134.3108}]

        for data in sunpos_test_data:
            azimuth, elevation = sp.sunpos(latitude = data["latitude"],
                                           longitude = data["longitude"],
                                           timezone = data["timezone"],
                                           year = data["year"],
                                           month = data["month"],
                                           day = data["day"],
                                           hour = data["hour"],
                                           minute = data["minute"],
                                           second = data["second"],
                                           refraction = data["refraction"])

            self.assertAlmostEqual(azimuth, data["azimuth"], places = 3)
            self.assertAlmostEqual(elevation, data["elevation"], places = 3)
        pass       