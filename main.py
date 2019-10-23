"""Main module"""
import logging

from metclient.frost import auth
from metclient.geo_locations import GeoLocation

# Add basic logger
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

session = auth.Session(config_file='config/config.ini', logger=logger)
poly = GeoLocation(place_id=198727066) # Oslo municipality

params = {
    "referencetime": "latest",
    "maxage": "P1M",
    "geometry": poly.get_simplified_wkt(max_char_size=1800)
}

df = session.get_data_frame(endpoint_type='lightning', dict_params=params)

print(df.head())