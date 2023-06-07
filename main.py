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
    args = parser.parse_args()

    debug_trace = args.debug_trace
    no_trace = args.no_trace
    log_filename = args.log_filename
    logger_level = logging.CRITICAL if no_trace else logging.DEBUG if debug_trace else logging.INFO
    logger_file = log_filename if log_filename else APP_LOGGING_FILE_NAME
    app = create_info_jobs_api(log_filename=logger_file, log_level=logger_level)
    app.get_jobs()


