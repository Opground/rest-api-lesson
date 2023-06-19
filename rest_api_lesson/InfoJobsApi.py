from rest_api_lesson.config.AppConfig import AppConfig, create_config
from rest_api_lesson.logger.AppLogger import init_logger
import logging
import os
import requests

class JobOffer:
    def __init__(self, title, category, subcategory, city, province, salaryMin, salaryMax, salaryPeriod, experienceMin):
        self.title = title
        self.category = category
        self.subcategory = subcategory
        self.city = city
        self.province = province
        self.salaryMin = salaryMin
        self.salaryMax = salaryMax
        self.salaryPeriod = salaryPeriod
        self.experienceMin = experienceMin

    def __str__(self):
        return f"Title: {self.title} Location: {self.city}, {self.province} Category: {self.category}"

class InfoJobsApi:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def get_jobs(self, category_param=None, subcategory_param=None, city_param=None, province_param=None, salaryMin_param=None, salaryMax_param=None, experienceMin_param=None) -> list[JobOffer]:
        
        # Constructs URL based on parameters passed and if they are valid
        parameters = []
        base_url = "https://api.infojobs.net/api/9/offer"
        if category_param is not None and self.verify_parameter(category_param, "category"):
            parameters.append(f"category={category_param}")
        if subcategory_param is not None and self.verify_parameter(subcategory_param, "subcategory"):
            parameters.append(f"subcategory={subcategory_param}")
        if city_param is not None and self.verify_parameter(city_param, "city"):
            parameters.append(f"city={city_param}")
        if province_param is not None and self.verify_parameter(province_param, "province"):
            parameters.append(f"province={province_param}")
        if salaryMin_param is not None:
            parameters.append(f"salaryMin={salaryMin_param}")
        if salaryMax_param is not None:
            parameters.append(f"salaryMax={salaryMax_param}")
        if experienceMin_param is not None and self.verify_parameter(experienceMin_param, "experience-min"):
            parameters.append(f"experienceMin={experienceMin_param}")
        if parameters:
            base_url += "?" + parameters[0]
            base_url += "&" + "&".join(parameters[1:])
        else:
            raise ValueError

        payload = {}
        headers = {
            'Authorization': f"Basic {self._config.get_setting('infojobs_api_key')}"
        }

        # Make request to /offer endpoint
        response = requests.request("GET", base_url, headers=headers, data=payload)

        # Check status code
        if response.status_code == 200:
            job_data = response.json()
            
            # Page vars for iterating through all offers 
            current_page = job_data.get('currentPage')
            total_pages = job_data.get('totalPages')

            # Create JobOffer object for each job listing and add to the list
            job_offers = []
            while current_page <= total_pages:
                for job in job_data['items']:
                    title = job.get('title')
                    category = job.get('category').get('value')
                    subcategory = job.get('subcategory').get('value')
                    city = job.get('city')
                    province = job.get('province').get('value')
                    salaryMin = job.get('salaryMin').get('value')
                    salaryMax = job.get('salaryMax').get('value')
                    salaryPeriod = job.get('salaryPeriod').get('value')
                    experienceMin = job.get('experienceMin').get('value')
                    
                    job_offer = JobOffer(title, category, subcategory, city, province, salaryMin, salaryMax, salaryPeriod, experienceMin)
                    job_offers.append(job_offer)
                
                # Iterate through each page of job offers
                current_page += 1
                if category_param and city_param and province_param and salaryMin_param and salaryMax_param is None:
                    param_url = base_url + "?page=" + str(current_page)
                else:
                    param_url = base_url + "&page=" + str(current_page)
                
                response = requests.request("GET", param_url, headers=headers, data=payload)
                job_data = response.json()

            return job_offers
        else:
            raise ValueError("Status code: {response.status_code}")


    # Verify parameter by comparing parameter input with dictionary
    def verify_parameter(self, parameter, parameter_type) -> bool:
        dictionary_url = f"https://api.infojobs.net/api/1/dictionary/{parameter_type}"
        
        payload = {}
        headers = {
            'Authorization': f"Basic {self._config.get_setting('infojobs_api_key')}"
        }

        response = requests.request("GET", dictionary_url, headers=headers, data=payload)

        if response.status_code == 200:
            dictionary_data = response.json()

            for dictionary_entry in dictionary_data:
                if parameter == dictionary_entry.get('value'):
                    return True
        
            return False


def create_info_jobs_api(log_filename: str = "melanoma_phd.log",
    log_level: int = logging.DEBUG,
    data_folder: str = None) -> InfoJobsApi:
    config = create_config(data_folder)
    log_filename = os.path.join(config.log_folder, log_filename)
    init_logger(log_filename, log_level)
    return InfoJobsApi(config)