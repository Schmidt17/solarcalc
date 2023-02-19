from solar_calculation.solar_benefits import calculate_solar_benefits
import solar_calculation.solar_cell as sc
import unittest
import pandas as pd
from datetime import datetime

class TestProcess(unittest.TestCase):

    def test_processing_one_year(self):
        cycles = 5
        stopwatch_start = datetime.now()
        for i in range(cycles):
             sc1 = sc.SolarCell(inclination = 30, azimuth = 180, pkpower_kW = 1)
             results = calculate_solar_benefits(latitude = 50.7913,
                                  longitude = 13.737262,
                                  timezone = 1,
                                  start_day = pd.Timestamp(2015, 1,1),
                                  end_day = pd.Timestamp(2015,7,1),
                                  solar_cells = [sc1],
                                  energy_cost  = 0.4)
        stopwatch_end = datetime.now()

        processing_time = (stopwatch_end - stopwatch_start) / 5

        print(f"Processing took {processing_time} for 1 year calculation\n"
              f"results are: {results}")