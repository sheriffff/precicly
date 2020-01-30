import requests


def shout(func):
    def wrapper(*args, **kwargs):
        print(f'Executing {func.__name__}')
        return func(*args, **kwargs)

    return wrapper


class BiciBcn():
    """
    Documentation for BiciBcn:
    Class in charge of connecting to Bicing Barcelona API and querying
    information.
    """

    url_get_all_stations_info = "http://wservice.viabicing.cat/v2/stations"

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
                f'The status code of request to {url} was {response.status_code}'
            )

        response_json = response.json()
        return response_json

    @shout
    def get_stations_dataframe(self) -> list:
        """
        Automatically contact the Bicing API and return the JSON
        field containing the stations data.
        """

        print("Contacting the Bicing API")
        data_json = self._get(self.url_get_all_stations_info).get("stations")
        print("Data successfully obtained")

        return data_json


# For testing
bicing_bcn = BiciBcn()
res = bicing_bcn.get_stations_dataframe()
