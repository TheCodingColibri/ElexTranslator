import json
from elex_string_table import ElexStringTable


class Config:
    def __init__(self):
        with open("config.json", "r") as config_file:
            config_json = json.load(config_file)
            self.source_string_table = ElexStringTable(config_json["source"]["file"], config_json["source"]["name"])
            self.compare_string_table = ElexStringTable(config_json["compare"]["file"], config_json["compare"]["name"])
            self.target_string_table_default = ElexStringTable(config_json["default_for_target"]["file"], config_json["default_for_target"]["name"])
            self.target_string_table = ElexStringTable(config_json["default_for_target"]["file"], config_json["default_for_target"]["name"])
            self.target = config_json["target"]