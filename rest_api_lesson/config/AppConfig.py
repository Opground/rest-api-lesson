import os
from typing import Dict

from rest_api_lesson.config.JsonConfig import JsonConfig


class AppConfig(JsonConfig):
    def __init__(self, config_file: str, data_folder: str) -> None:
        super().__init__(config_file)
        self._name = self.get_setting("config/name")
        self._data_folder = os.path.join(data_folder, self._name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def data_folder(self) -> str:
        return self._data_folder

    @property
    def log_folder(self) -> str:
        return os.path.join(self.data_folder, "log")

def create_config(data_folder=None) -> AppConfig:
    """
    Creates the configuration object for the application.
    """
    folder_name = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(folder_name, "config.json")
    if not data_folder:
        data_folder = os.path.join(folder_name, "../../", "data")
    config = AppConfig(config_file, data_folder)
    print(f"'{config.name}' environment has been configured successfully", flush=True)
    return config
