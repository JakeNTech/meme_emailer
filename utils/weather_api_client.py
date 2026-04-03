import requests

from utils import constants

class weather_client():
    def __init__(self, token):
        self.api_root = constants.WEATHER_API_ROOT
        self.token = token
        self.current_weather_json = None

    def _extract_weather_for_email(self):
        return self.current_weather_json['current']['temp_c'], self.current_weather_json['current']['condition']['text']

    def get_location_weather(self, location):
        url = self.api_root + "/v1/current.json"
        params = {
            "q": location,
            "key": self.token
        }
        r = requests.get(url, params=params)
        if (r.status_code == 200):
            self.current_weather_json = r.json()
        else:
            print(r.status_code, r.text)