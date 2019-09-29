"""Module for getting Polygons."""
import logging
import requests
from shapely.geometry import Polygon


class GeoLocation:
    """Class for getting polygons."""

    OPEN_STREET_MAP_BASE_ENDPOINT = "https://nominatim.openstreetmap.org/details.php"
    PARAMS = {
        'polygon_geojson': 1,
        'format': 'json'
    }

    def __init__(self, place_id, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.params = GeoLocation.PARAMS
        self.polygon = None
        self.place_id = place_id

    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, place_id):
        """
        Return a polygon from the given place_id.
        :return: string
        """
        self._place_id = place_id
        self.params['place_id'] = place_id

        response = requests.get(
            url=GeoLocation.OPEN_STREET_MAP_BASE_ENDPOINT,
            params=self.params
        )

        geo_data = response.json()
        coordinates = geo_data['geometry']['coordinates']
        assert len(coordinates) == 1, "Single polygon required."
        self.polygon = Polygon(coordinates[0])
        assert self.polygon.is_valid, "Not a valid Polygon"

    def get_simplified_wkt(self, max_char_size, tolerance=0.001, tolerance_increment=0.0005):
        """
        Simplify polygon and return the wkt representation of it.
        :param tolerance_increment:
        :param tolerance:
        :param max_char_size:
        :return: wkt representation of simplified polygon
        """
        poly = self.polygon

        while len(poly.wkt)>max_char_size:
            poly = poly.simplify(tolerance=tolerance)
            tolerance += tolerance_increment

        return poly.wkt


class PlaceIdSearch:
    """Class used for searching for place_id."""
    @staticmethod
    def search_place_id(self, location):
        #  Search for place_id for the location
        pass