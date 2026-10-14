                               
import json


class Conf:
    def __init__(self, confPath):
        with open(confPath, encoding="utf-8") as config_file:
            self.__dict__.update(json.load(config_file))

    def __getitem__(self, k):
        return self.__dict__.get(k, None)