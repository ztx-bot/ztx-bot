import json

def get_config(key: str):
    with open('config.json','r') as f:
        return json.load(f)[key]