import requests

from madrid.auth_credentials import auth_bicimad


def shout(func):
    def wrapper(*args, **kwargs):
        print(f'Executing {func.__name__}')
        return func(*args, **kwargs)

    return wrapper


class BiciMad:
    """
    Class in charge of connecting to BiciMad API and querying information
    Documentation here: https://apidocs.emtmadrid.es/
    """
    url_login = 'https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/'
    url_logout = 'https://openapi.emtmadrid.es/v1/mobilitylabs/user/logout/'
    url_who_am_i = 'https://openapi.emtmadrid.es/v1/mobilitylabs/user/whoami/'
    url_get_all_stations_info = 'https://openapi.emtmadrid.es/v1/transport/bicimad/stations/'

    stations_keys = ['id', 'number', 'activate', 'total_bases', 'dock_bikes', 'free_bases', 'reservations_count']

    def __init__(self):
        self._load_access_token()

    @staticmethod
    def _get(url: str, headers: dict, timeout: float = 3) -> dict:
        """
        Wrapper of requests.get checking status_code
        Args:
            url: url to GET
            headers: headers of the request
            timeout: time to wait for response

        Returns:
            dictionary with json content
        """
        response = requests.get(
            url=url,
            headers=headers,
            timeout=timeout
        )

        if response.status_code != 200:
            raise requests.HTTPError(f'The status code of request to {url} was {response.status_code}')

        response_json = response.json()

        return response_json

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

        response_json = self._get(url=self.url_login, headers=auth_bicimad)

        if (code := response_json.get('code')) == '00':
            self.access_token = response_json.get('data')[0].get('accessToken')
            self._save_access_token()

        elif code == '01':
            print('Logging out...')
            self.access_token = response_json.get('description').split()[1]
            self._save_access_token()
            self._logout()
            self._get_access_token()

    @shout
    def _logout(self):
        """
        Calls API to logout
        """
        self._get(url=self.url_logout, headers={'accessToken': self.access_token})

    @shout
    def _is_access_token_alive(self):
        """
        Checks if current access token works
        """
        if self.access_token is None:
            return False

        response_json = self._get(url=self.url_who_am_i, headers={'accessToken': self.access_token})

        if response_json.get('code') != '02':
            return False
        else:
            return True

    @shout
    def _save_access_token(self):
        """)
        Saves access token to file
        """
        open('access_token.txt', 'w+').write(self.access_token)

    @shout
    def get_stations_info(self):
        """
        Calls API and gets all stations' status
        """
        response_json = self._get(url=self.url_get_all_stations_info, headers={'accessToken': self.access_token})

        if response_json.get('code') != '00':
            print('Invalid token... lets get a new one')
            self._get_access_token()

            return self.get_stations_info()

        datetime = response_json.get('datetime')[:-7]
        data = response_json.get('data')
        # lets create a state to compare consecutive queries, because sometimes nothing changes
        state = hash(str(data))

        for station in data:
            station['datetime'] = datetime
            station['lon'], station['lat'] = station.get('geometry').get('coordinates')
            del station['geometry']

        return data, state
