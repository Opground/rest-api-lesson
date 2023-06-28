from rest_api_lesson.config.AppConfig import create_config

import argparse
import logging

from rest_api_lesson.InfoJobsApi import create_info_jobs_api

APP_LOGGING_FILE_NAME = "rest_api_lesson.log"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InfoJobs job retrieval application")
    parser.add_argument("--debug_trace", action="store_true", help="print all logging messages")
    parser.add_argument("--no_trace", action="store_true", help="no logging messages")
    parser.add_argument("--log_filename", metavar="log_filename", help="filename of the logs")
    parser.add_argument("--keyword", metavar="keyword", help="keyword parameter")
    parser.add_argument("--category", metavar="category", help="category parameter")
    parser.add_argument("--subcategory", metavar="subcategory", help="subcategory parameter")
    parser.add_argument("--city", metavar="city", help="city parameter")
    parser.add_argument("--province", metavar="province", help="province parameter")
    parser.add_argument("--salaryMin", metavar="salaryMin", help="minimum salary parameter")
    parser.add_argument("--salaryMax", metavar="salaryMax", help="maximum salary parameter")
    parser.add_argument("--experienceMin", metavar="experienceMin", help="minimum experience parameter")
    parser.add_argument("--dummy", action="store_true", help="dummy data parameter")
    args = parser.parse_args()

    debug_trace = args.debug_trace
    no_trace = args.no_trace
    log_filename = args.log_filename
    logger_level = logging.CRITICAL if no_trace else logging.DEBUG if debug_trace else logging.INFO
    logger_file = log_filename if log_filename else APP_LOGGING_FILE_NAME
    app = create_info_jobs_api(log_filename=logger_file, log_level=logger_level)
    job_offers = app.get_jobs(args)
    
    for job in job_offers:
        print(job)
