import json
import os
from pathlib import Path


def get_google_token(token_path=None):
    if not token_path:
        if os.environ["G_TOKEN"]:
            to_return = json.loads(os.environ["G_TOKEN"])
        else:
            print("No Google Refresh Token found!")
    else:
        with Path.open(token_path, "r") as f:
            to_return = json.load(f)
    return(to_return)

def get_wether_token(token_path=None):
    if not token_path:
        if os.environ["WEATHER_TOKEN"]:
            to_return = json.loads(os.environ["WEATHER_TOKEN"])
        else:
            print("No weather api Token found!")
    else:
        with Path.open(token_path, "r") as f:
            to_return = f.read()
    return(to_return)

def get_config(config_path=None):
    if not config_path:
        if os.environ["CONFIG_JSON"]:
            to_return = json.loads(os.environ["CONFIG_JSON"])
        else:
            print("No Config JSON Found")
    else:
        with Path.open(config_path, "r") as f:
            to_return = json.load(f)
    return(to_return)
