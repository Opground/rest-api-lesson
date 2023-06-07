from rest_api_lesson.config.AppConfig import AppConfig, create_config
from rest_api_lesson.logger.AppLogger import init_logger
import logging
import os

class InfoJobsApi:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def get_jobs(self) -> None:
        #TODO: Get jobs from InfoJobs REST API
        # TIP: Get API key from config -> config.get_setting('infojobs_api_key')
        raise NotImplementedError("Getting jobs from InfoJobs portal not implemented yet!")

def create_info_jobs_api(log_filename: str = "melanoma_phd.log",
    log_level: int = logging.DEBUG,
    data_folder: str = None) -> InfoJobsApi:
    config = create_config(data_folder)
    log_filename = os.path.join(config.log_folder, log_filename)
    init_logger(log_filename, log_level)
    return InfoJobsApi(config)