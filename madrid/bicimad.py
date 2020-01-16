import requests
import pandas as pd

from madrid.auth_credentials import auth_bicimad


def shout(func):
    def wrapper(*args, **kwargs):
        print(f'Executing {func.__name__}')
        return func(*args, **kwargs)

    return wrapper


class BiciMad:
    """
    Class in charge of connecting to BiciMad API and querying information
    """
    url_login_bicimad = 'https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/'
    url_who_am_i = 'https://openapi.emtmadrid.es/v1/mobilitylabs/user/whoami/'
    url_get_all_stations_info = 'https://openapi.emtmadrid.es/v1/transport/bicimad/stations/'
    stations_keys = ['id', 'number', 'activate', 'total_bases', 'dock_bikes', 'free_bases', 'reservations_count']

    def __init__(self):
        self._load_access_token()

    @shout
    def _load_access_token(self):
        """
        Loads working access token into self
        """
        try:
            self.access_token = open('access_token.txt', 'r').read()
        except FileNotFoundError:
            self.access_token = None

        if (self.access_token is None) or (not self._is_access_token_alive()):
            self._get_access_token()

    @shout
    def _get_access_token(self):
        """
        Calls API to get new access token
        """
        print('Getting access token...')

        response = requests.get(
            url=self.url_login_bicimad,
            headers=auth_bicimad,
            timeout=3
        )

        self.access_token = response.json().get('data')[0].get('accessToken')
        self._save_access_token()

    @shout
    def _is_access_token_alive(self):
        """
        Checks if current access token works
        """
        if self.access_token is None:
            return False

        response = requests.get(
            url=self.url_who_am_i,
            headers={'accessToken': self.access_token},
            timeout=3
        )

        return response.json().get('code') == '02'

    @shout
    def _save_access_token(self):
        """
        Saves access token to file
        """
        open('access_token.txt', 'w+').write(self.access_token)

    @shout
    def get_stations_info(self):
        """

        Calls API and gets all stations' status
        # TODO ideally this will save into file or ddbb, for the moment returns pd.DataFrame for testing
        Returns:
        # TODO we are using google documentation for functions. I have yet to see how return tuples are documented
            tuple:
                int
                pd.DataFrame
        """

        response = requests.get(
            url=self.url_get_all_stations_info,
            headers={'accessToken': self.access_token},
            timeout=3
        )

        response_json = response.json()

        if response_json.get('code') != '00':
            print('Invalid token... lets get new one')
            self._get_access_token()

            return self.get_stations_info()

        n_stations = int(response_json.get('description')[:3])

        df = pd.DataFrame(response_json.get('data'))[self.stations_keys]
        df['datetime'] = pd.to_datetime(response_json.get('datetime'))

        return n_stations, df
