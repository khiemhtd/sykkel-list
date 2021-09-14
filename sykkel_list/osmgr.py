import json
import logging

from urllib.request import Request, urlopen

LOGGER = logging.getLogger(__name__)

# May want to move into separate file since it's used by multiple files, could cause import loop
FIELD_DATA = "data"
FIELD_STATIONS = "stations"
FIELD_STATION_ID = "station_id"
FIELD_NAME = "name"
FIELD_NUM_BIKES_AVAILABLE = "num_bikes_available"
FIELD_NUM_DOCKS_AVAILABLE = "num_docks_available"

class OsloSykkelManager:
    '''
    OsloSykkelManager can retrieve real-time Oslo Sykkel data by sending HTTP requests.
    For convenience it also has an option to create a dict to keep all bike station
    related data together in one dictionary and accessible by station id. Use self.stations
    to access the data, it'll look something like this:
    {
        "2315":{
            "station_id":"2315",
            "name":"Rostockgata",
            "address":"Rostockgata 5",
            "rental_uris":{
                "android":"oslobysykkel://stations/2315",
                "ios":"oslobysykkel://stations/2315"
            },
            "lat":59.90688962048543,
            "lon":10.76030652299994,
            "capacity":18,
            "is_installed":1,
            "is_renting":1,
            "is_returning":1,
            "last_reported":1631605553,
            "num_bikes_available":18,
            "num_docks_available":0
        },
        "2309":{
            "station_id":"2309",
            "name":"Ulven Torg",
            "address":"Ulvenveien 89",
            "rental_uris":{
                "android":"oslobysykkel://stations/2309",
                "ios":"oslobysykkel://stations/2309"
            },
            "lat":59.924959978447504,
            "lon":10.812061140924698,
            "capacity":30,
            "is_installed":1,
            "is_renting":1,
            "is_returning":1,
            "last_reported":1631605553,
            "num_bikes_available":14,
            "num_docks_available":16
        },
        ....
    }
    '''
    API_ID = "placeholder-id"
    HEADERS = { "Client-Identifier" : API_ID, "content-type" : "application/json" }
    URL_STATION_INFO = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
    URL_STATION_STATUS = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"

    def __init__(self):
        self.stations = {}
        self._initialize_stations()

    def _initialize_stations(self):
        '''
        Initialize self.stations with values from station_info endpoint.
        station_info data is static so only needs to be called once
        '''
        station_info = self.get_station_info().get(FIELD_DATA, {}).get(FIELD_STATIONS, {})
        self._update_stations(station_info)

    def _update_stations(self, stations_list):
        '''
        Update self.stations with values from stations_list
        :param stations_list: List or dict containing station data
        '''
        # If dict, attempt to retrieve list of stations
        if isinstance(stations_list, dict):
            LOGGER.warning(f"{self._update_stations.__name__}: stations_list is a dict, attempting to retrieve list of stations")
            stations_list = stations_list.get(FIELD_DATA, {}).get(FIELD_STATIONS, {})

        if not isinstance(stations_list, list):
            LOGGER.error(f"Could not update stations, not a list: {stations_list}")
            return

        # Merge/update the station data i.e. stations[station_id] union station
        for station in stations_list:
            station_id = station.get(FIELD_STATION_ID, None)
            if station_id:
                self.stations[station_id] = { **self.stations.get(station_id, {}), **station }

    def _convert_result_to_json(self, result) -> dict:
        if result == {}:
            return result
        try:
            return json.loads(result)
        except Exception as e:
            LOGGER.error("Could not convert {result} to json: {e}")
            return {}

    def send_request(self, url:str, headers:dict = HEADERS, timeout=5) -> str:
        req = Request(url, headers=headers)
        try:
            return urlopen(req, timeout=5).read().decode('utf-8')
        except Exception as e:
            LOGGER.error(f"Could not connect to {url}: {e}")
            return {}

    def get_station_info(self) -> dict:
        result = self.send_request(OsloSykkelManager.URL_STATION_INFO)
        data = self._convert_result_to_json(result)
        return data

    def get_station_status(self) -> dict:
        result = self.send_request(OsloSykkelManager.URL_STATION_STATUS)
        data = self._convert_result_to_json(result)
        return data

    def update_station_status(self) -> dict:
        station_status = self.get_station_status().get(FIELD_DATA, {}).get(FIELD_STATIONS, {})
        self._update_stations(station_status)

