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

    def get_jobs(self, args) -> list[JobOffer]:
       
        # Constructs URL based on parameters passed and if they sare valid
        base_url = "https://api.infojobs.net/api/9/offer"
        parameters = []

        if hasattr(args, 'category') and args.category is not None and self.verify_parameter(args.category, "category"):
            parameters.append(f"category={args.category}")
        if hasattr(args, 'subcategory') and args.subcategory is not None and self.verify_parameter(args.subcategory, "subcategory"):
            parameters.append(f"subcategory={args.subcategory}")
        if hasattr(args, 'city') and args.city is not None and self.verify_parameter(args.city, "city"):
            parameters.append(f"city={args.city}")
        if hasattr(args, 'province') and args.province is not None and self.verify_parameter(args.province, "province"):
            parameters.append(f"province={args.province}")
        if hasattr(args, 'salaryMin') and args.salaryMin is not None:
            parameters.append(f"salaryMin={args.salaryMin}")
        if hasattr(args, 'salaryMax') and args.salaryMax is not None:
            parameters.append(f"salaryMax={args.salaryMax}")
        if hasattr(args, 'experienceMin') and args.experienceMin is not None and self.verify_parameter(args.experienceMin, "experience-min"):
            parameters.append(f"experienceMin={args.experienceMin}")
        if len(parameters) != 0:
            base_url += "?" + parameters[0]
            base_url += "&" + "&".join(parameters[1:])

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
                if len(parameters) == 0:
                    param_url = base_url + "?page=" + str(current_page)
                else:
                    param_url = base_url + "&page=" + str(current_page)
                
                response = requests.request("GET", param_url, headers=headers, data=payload)
                job_data = response.json()

            return job_offers
        else:
            raise ValueError(f"Status code: {response.status_code}")


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

            raise ValueError(f"{parameter} is invalid {parameter_type}.")


def create_info_jobs_api(log_filename: str = "melanoma_phd.log",
    log_level: int = logging.DEBUG,
    data_folder: str = None) -> InfoJobsApi:
    config = create_config(data_folder)
    log_filename = os.path.join(config.log_folder, log_filename)
    init_logger(log_filename, log_level)
    return InfoJobsApi(config)