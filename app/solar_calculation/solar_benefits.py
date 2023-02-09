"""
 module for calculation of the benefits of a solar system
"""

import pandas as pd
import solar_calculation.solar_cell as sol

def calculate_solar_benefits(latitude: float,
                             longitude: float,
                             start_day: pd.Timestamp,
                             end_day: pd.Timestamp,
                             solar_cells: list,
                             timezone: int=1,
                             energy_cost: float = 0.4) ->dict:
    """ calculates the benefits of given solar system and returns the summary as dict 

    Note that in current demo state only sun minutes of 2016 are available and weather data
    is not yet based on location.

    """

    pwr_tbl = sol.generate_solar_power_table(latitude=latitude,
                                             longitude =longitude,
                                             timezone=timezone,
                                             start_day=start_day,
                                             end_day=end_day,
                                             solar_cells = solar_cells)

    # calculate total produced solar energy
    gen_sol_energy = pwr_tbl["solar_power"].sum()
    print(f"With given inputs you have generated {gen_sol_energy:.1f} kWh solar energy")

    # calculate expected savings
    self_use_ratio = 0.3
    savings = gen_sol_energy * self_use_ratio * energy_cost
    print(f"You made savings of {savings:.2f} EUR by using {self_use_ratio*100} % of your produced solar energy")

    return {"gen_sol_energy": gen_sol_energy,
            "savings": savings}