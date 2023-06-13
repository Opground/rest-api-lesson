from rest_api_lesson.config.AppConfig import AppConfig, create_config
from rest_api_lesson.logger.AppLogger import init_logger
import logging
import os
import requests

class JobOffer:
    def __init__(self, title, province, city, category):
        self.title = title
        self.city = city
        self.province = province
        self.category = category

    def __str__(self):
        return f"Title: {self.title} Location: {self.city}, {self.province} Category: {self.category}"

class InfoJobsApi:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def get_jobs(self) -> list[JobOffer]:
        url = "https://api.infojobs.net/api/9/offer"

        payload = {}
        headers = {
            'Authorization': f"Basic {self._config.get_setting('infojobs_api_key')}"
        }

        # Make request to /offer endpoint
        response = requests.request("GET", url, headers=headers, data=payload)

        # Check status code
        if response.status_code == 200:
            job_data = response.json()

            #TODO: Iterate through all pages using following vars
            current_page = job_data.get('currentPage')
            page_size = job_data.get('pageSize')
            total_pages = job_data.get('totalPages')
            
            # Create JobOffer object for each job listing and add to the list
            job_offers = []
            for job in job_data['items']:
                title = job.get('title')
                city = job.get('city')
                province = job.get('province').get('value')
                category = job.get('category').get('value')
                job_offer = JobOffer(title, province, city, category)
                job_offers.append(job_offer)
            return job_offers
        else:
            raise ValueError("Status code: {response.status_code}")

        # TIP: Get API key from config -> config.get_setting('infojobs_api_key')
        # raise NotImplementedError("Getting jobs from InfoJobs portal not implemented yet!")

def create_info_jobs_api(log_filename: str = "melanoma_phd.log",
    log_level: int = logging.DEBUG,
    data_folder: str = None) -> InfoJobsApi:
    config = create_config(data_folder)
    log_filename = os.path.join(config.log_folder, log_filename)
    init_logger(log_filename, log_level)
    return InfoJobsApi(config)