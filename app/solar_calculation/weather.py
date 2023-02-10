import pandas as pd
import pathlib


# pre-load the example weather data for fast response time
data_file = pathlib.Path(__file__).parent / "weather_data" / "sun_m_per_h_Rochlitz_2016.csv"
data = pd.read_csv(data_file, usecols=["Zeitstempel","Wert"], index_col = False)
data["timestamp"] = data["Zeitstempel"].apply(pd.Timestamp)


def get_sun_minutes(start_day, end_day) -> pd.DataFrame:
    """ returns a DataFrame with the sun minutes per hour within the given time range 
    
    this is currently not distinguishing the location!

    """

    data_subset = data.query(" timestamp >= @start_day and timestamp <= @end_day")
    data_subset = data_subset.rename(columns={"Wert": "sun_minutes"})
    
    sun_minutes = data_subset.xs(["timestamp", "sun_minutes"], axis = 1)
    return sun_minutes



