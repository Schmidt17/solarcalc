import pandas as pd
import pathlib


# pre-load the example weather data for fast response time
print("Loading weather data")
data_file = pathlib.Path(__file__).parent / "weather_data" / "sun_m_per_h_Rochlitz_2016.csv"
data = pd.read_csv(data_file, usecols=["Zeitstempel","Wert"], index_col = False)

data["timestamp"] = data["Zeitstempel"].apply(pd.Timestamp)
# the day of year is used for matching the loaded data with the requested time range,
# which might be from different years
data["day_of_year"] = data["timestamp"].dt.day_of_year
data = data.rename(columns={"Wert": "sun_minutes"})


def get_sun_minutes(start_day, end_day) -> pd.DataFrame:
    """ returns a DataFrame with the sun minutes per hour within the given time range 
    
    This is currently not distinguishing the location!

    This also currently uses the sun minutes of the corresponding date range in 2016
    instead of the exact requested year. Both start and end day are included.

    """
    # create a list of the days of year for the requested range, to match with the 2016 sun minutes data
    dates = pd.date_range(start_day, end_day)
    dates_df = pd.DataFrame({'timestamp_day': dates})
    dates_df['day_of_year'] = dates_df['timestamp_day'].dt.day_of_year

    data_matched = dates_df.merge(data, on='day_of_year', how='inner',
                                  suffixes=('_date', ''))  

    sun_minutes = data_matched[["timestamp", "sun_minutes"]].copy()

    start_offset = start_day - sun_minutes["timestamp"].min()
    sun_minutes["timestamp"] = sun_minutes["timestamp"] + start_offset

    return sun_minutes



