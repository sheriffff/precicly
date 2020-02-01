import requests
import json
import pandas as pd
from datetime import datetime


def shout(func):
    def wrapper(*args, **kwargs):
        print(f'Executing {func.__name__}')
        return func(*args, **kwargs)

    return wrapper


class BiciBcn():
    """
    Documentation for BiciBcn:
    Class in charge of connecting to Bicing Barcelona API and Weather API.
    """

    url_get_all_stations_info = "http://wservice.viabicing.cat/v2/stations"

    # This JSON contains all stations with id, location, etc..
    # Can be downloaded from http://bulk.openweathermap.org/sample/
    available_cities_weather = "../city_list.json"

    # Barcelona square defined at http://bboxfinder.com/
    square = [2.104912, 41.354778, 2.224045, 41.447873]

    # rstrip to remove trailing lines
    api_key = open('weather_barcelona_token.txt', 'r').read().rstrip()

    def __init__(self):
        pass

    @staticmethod
    def _get(url: str, timeout: float = 3) -> dict:
        """
        Wrapper around request.get to request the JSON with all available
        bicycle information from Bicing Barcelona.
        """

        response = requests.get(url=url, timeout=timeout)

        if response.status_code != 200:
            requests.HTTPError(
                f"The status code of request to {url} was {response.status_code}"
            )

        response_json = response.json()
        return response_json

    @shout
    def get_stations(self) -> list:
        """
        Automatically contact the Bicing API and return the JSON
        field containing the stations data.
        """

        print("Contacting the Bicing API")
        data_json = self._get(self.url_get_all_stations_info).get("stations")
        print("Data successfully obtained")
        return data_json

    @staticmethod
    def _within_square(square: list, point: list) -> bool:
        """
        Checks whether point is within the square. This is useful for
        identifying the coordinates of a given point are within a square.

        Here it's used to identify which weather stations are within the
        square of Barcelona.
        """
        within1 = (square[0] < point[0] < square[2])
        within2 = (square[1] < point[1] < square[3])
        within = within1 and within2

        return within

    @shout
    def _grab_cities(self) -> list:
        """
        Reads the available weather stations from the JSON of the weather API
        and extracts the stations that are within the square defined
        for Barcelona. It returns a list where each slot is a dictionary
        with information related to that weather stations (id, coordinates,
        etc...)
        """

        # Grab all cities available in weather map
        with open(self.available_cities_weather, "r") as f:
            cities = json.load(f)

        # Only keep the ones that are within the square of Barcelona
        # Tried a list comprehension but too long
        bcn_cities = []
        for i in cities:
            if self._within_square(self.square, list(i.get("coord").values())):
                bcn_cities.append(i)

        return bcn_cities

    @staticmethod
    def _wrangle_weather(weather_dict: dict) -> pd.DataFrame:
        """
        Given the response of the weather API, wrangle and transform
        the dictionary to a data frame. The meaning of each field from
        the weather API can be found at https://openweathermap.org/current

        The current fields are:
        'id'
        'weather.id'
        'weather.main'
        'weather.description'
        'weather.icon'
        'main.temp'
        'main.feels_like'
        'main.temp_min'
        'main.temp_max'
        'main.pressure'
        'main.humidity'
        'wind.speed'
        'clouds.all'
        'rain.1h'
        'rain.3h'
        'snow.1h'
        'snow.3h'
        'wind.deg'
        'timestamp'
        """

        # Meaning of each field is here https://openweathermap.org/current
        # The meaning of weather icons is
        # https://openweathermap.org/weather-conditions
        parts_dict = ["weather", "main", "wind", "clouds"]

        all_dict = []
        # Iterate over each field in the response and update the name of each
        # field. I do this to match the names of the fields from the actual
        # documentation.
        for i in parts_dict:
            if i in "weather":
                all_dict.append({i + "." + n: v for n, v in weather_dict.get(i)[0].items()})
            else:
                all_dict.append({i + "." + n: v for n, v in weather_dict.get(i).items()})

        # In case the field is empty, which it is currently
        empty_rain = {"1h": pd.np.nan, "3h": pd.np.nan}
        rain = {"rain." + n: v for n, v in weather_dict.get("rain", empty_rain).items()}

        # In case the field is empty, which it is currently
        empty_snow = {"1h": pd.np.nan, "3h": pd.np.nan}
        snow = {"snow." + n: v for n, v in weather_dict.get("snow", empty_snow).items()}

        # Note: this is the time when the measurement was taken (not when the
        # API request was done). This should be the time at which you match
        # weather data to bicycle stations.
        timestamp = datetime.fromtimestamp(weather_dict.get("dt"))
        date = {"date": timestamp.strftime('%Y-%m-%d')}
        time = {"time": timestamp.strftime('%H:%M:%S')}

        for i in [rain, snow, date, time]:
            all_dict.append(i)

        # Insert the station ID at the beginning of the list
        all_dict.insert(0, {"id": weather_dict.get("id")})

        # Convert everything to a DataFrame
        all_dt = [pd.DataFrame([dt]) for dt in all_dict]
        weather_dt = pd.concat(all_dt, axis=1)

        return weather_dt

    @shout
    def get_weather(self) -> pd.DataFrame:
        """
        Using the available cities in Barcelona, request weather data for all
        stations and transform them into a data frame.
        """

        print("Grabbing available weather stations")
        bcn_cities = self._grab_cities()
        code_str = ",".join([str(i.get("id")) for i in bcn_cities])
        weather_url = 'http://api.openweathermap.org/data/2.5/group?'\
            f'id={code_str}&units=metric&appid={self.api_key}'

        print("Contacting the Weather API")
        weather_dict = self._get(url=weather_url).get("list")
        print("Data successfully obtained")

        print("Transforming weather data")
        cleaned_weather = [self._wrangle_weather(i) for i in weather_dict]
        weather_df = pd.concat(cleaned_weather, axis=0, sort=False)
        print("Transforming successfully transformed")

        return weather_df


# For testing
bicing_bcn = BiciBcn()
bicing_bcn.get_stations()
bicing_bcn.get_weather()
