from rest_api_lesson.config.AppConfig import AppConfig, create_config
from rest_api_lesson.logger.AppLogger import init_logger
from typing import Dict
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
        title_truncated = f"{self.title[:35]}..." if len(self.title) > 35 else self.title
        category_truncated = f"{self.category[:30]}..." if len(self.category) > 30 else self.category
        return f"Title: {title_truncated:38} Location: {self.city[:15]}, {self.province[:15]} Category: {category_truncated:33}"

class InfoJobsApi:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def get_jobs(self, args: Dict) -> list[JobOffer]:
       
        # Constructs URL based on parameters passed and if they sare valid
        base_url = "https://api.infojobs.net/api/9/offer"
        parameters = []

        if 'dummy' in args and args['dummy'] is True:
            return self.get_dummy_data()
        if 'keyword' in args and args['keyword'] is not None:
            parameters.append(f"q={args['keyword']}")
        if 'category' in args and args['category'] is not None and self.verify_parameter(args['category'], "category"):
            parameters.append(f"category={args['category']}")
        if 'subcategory' in args and args['subcategory'] is not None and self.verify_parameter(args['subcategory'], "subcategory"):
            parameters.append(f"subcategory={args['subcategory']}")
        if 'city' in args and args['city'] is not None and self.verify_parameter(args['city'], "city"):
            parameters.append(f"city={args['city']}")
        if 'province' in args and args['province'] is not None and self.verify_parameter(args['province'], "province"):
            parameters.append(f"province={args['province']}")
        if 'salaryMin' in args and args['salaryMin'] is not None:
            parameters.append(f"salaryMin={args['salaryMin']}")
        if 'salaryMax' in args and args['salaryMax'] is not None:
            parameters.append(f"salaryMax={args['salaryMax']}")
        if 'experienceMin' in args and args['experienceMin'] is not None and self.verify_parameter(args.experienceMin, "experience-min"):
            parameters.append(f"experienceMin={args['experienceMin']}")
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
        response.raise_for_status()
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
        
    def get_dummy_data(self) -> list[JobOffer]:
        dummy_offer1 = JobOffer("Job Title 1", "Category 1", "Subcategory 1", "City 1", "Province 1", "Minimum Salary 1", "Maximum Salary 1", "Salary Period 1", "Minimum Experience 1")
        dummy_offer2 = JobOffer("Job Title 2", "Category 2", "Subcategory 2", "City 2", "Province 2", "Minimum Salary 2", "Maximum Salary 2", "Salary Period 2", "Minimum Experience 2")
        dummy_offer3 = JobOffer("Job Title 3", "Category 3", "Subcategory 3", "City 3", "Province 3", "Minimum Salary 3", "Maximum Salary 3", "Salary Period 3", "Minimum Experience 3")

        return [dummy_offer1, dummy_offer2, dummy_offer3]
    

def create_info_jobs_api(log_filename: str = "rest_api_lesson.log",
    log_level: int = logging.DEBUG,
    data_folder: str = None) -> InfoJobsApi:
    config = create_config(data_folder)
    log_filename = os.path.join(config.log_folder, log_filename)
    init_logger(log_filename, log_level)
    return InfoJobsApi(config)