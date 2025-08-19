# config_loader.py

import yaml

class Config:
    def __init__(self, path="config.yaml"):
        with open(path, 'r') as f:
            self._cfg = yaml.safe_load(f)

    @property
    def mqtt(self):
        return self._cfg['mqtt']

    @property
    def valves(self):
        return self._cfg['valves']

    @property
    def pump(self):
        return self._cfg['pump']

    @property
    def general(self):
        return self._cfg['general']
