"""Module used for authentication."""
import requests
import configparser
import logging
from typing import Dict
from urllib.parse import urlencode
from pandas import DataFrame


from metclient.frost.lightning.lightning import Lightning


class ConfigException(Exception):
    pass


class ConfigMissingException(Exception):
    pass


class ApiEndpoints:
    BASE_FROST_ENDPOINT = "https://frost.met.no/"
    API_VERSION = 'v0'
    OUTPUT_FORMATS = ['jsonld', 'ualf']
    TYPE = [
        'observations', 'climatenormals', 'frequencies', 'records', 'lightning',
        'locations', 'elements', 'sources'
    ]

    @classmethod
    def lightning(cls):
        return ApiEndpoints.BASE_FROST_ENDPOINT + 'lightning/' + ApiEndpoints.API_VERSION + '.' + 'ualf'


class Auth:
    """
    Authentication
    """
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._validate()

    def _validate(self):

        auth = (self.client_id, self.client_secret)
        # TODO: Add validation step
        return True

    def get_auth(self):
        return self.client_id, self.client_secret


class Session(ApiEndpoints):

    def __init__(self, client_id=None, client_secret=None, config_file=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.auth = None
        if config_file:
            self.read_config_file(config_file)
        elif client_id and client_secret:
            self.config(client_id, client_secret)
        else:
            raise ConfigMissingException

        self._session = requests.Session()
        self._session.auth = self.auth.get_auth()

    def read_config_file(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.auth = Auth(
            config['credentials']['client_id'],
            config['credentials']['client_secret']
        )

    def config(self, client_id, client_secret):
        if self.auth:
            raise ConfigException('Session already configured.')
        self.auth = Auth(client_id, client_secret)

    def query(self, endpoint, params):
        response = self._session.get(endpoint +"?"+ urlencode(params))
        response.raise_for_status()
        return response

    def get_data_frame(self, endpoint_type: str, dict_params: Dict) -> DataFrame:
        """
        Return a dataframe
        :param endpoint_type: Required endpoint
        :type endpoint_type: str
        :param dict_params: dictionary with parameters of query
        :type dict_params: dict
        :return: data frame
        :rtype: DataFrame
        """
        if endpoint_type == 'lightning':
            response = self.query(
                self.lightning(),
                dict_params
            )
            return Lightning.get_df(response)
        elif endpoint_type in Session.TYPE:
            raise NotImplementedError
        else:
            raise ValueError(endpoint_type, " is not a valid input. Must be: ", Session.TYPE)

    def get_metadata(self):
        raise NotImplementedError

    def search(self):
        raise  NotImplementedError


