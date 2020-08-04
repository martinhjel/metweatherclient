"""Module for baseclient of the frost api."""

import requests


class BaseClient():
    BASE_FROST_ENDPOINT = "https://frost.met.no/"

    def __init__(self):
        pass

    @staticmethod
    def query(self, endpoint, params):
        """
        :param self:
        :return: results from HTML API Call
        """

        results = requests.get(
            endpoint,
            params=params,
            auth=(client_id, client_secret)
        )
