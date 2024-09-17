# appname/tasks.py

import logging
import time
import csv
import os
from celery import shared_task
from .models import Company

logger = logging.getLogger(__name__)
@shared_task
def process_uploaded_file(file_path):
    """
    Process the uploaded file asynchronously.
    The actual file processing logic (like parsing CSV, etc.) should be added here.
    """
    time.sleep(10) 
    print(f"Processing file: {file_path}")
    return "File processed successfully"


@shared_task
def process_csv(file_path):
    logger.info(f"Started processing the CSV file at: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row

            for row in reader:
                logger.info(f"Processing row: {row}")

                # Assuming your CSV columns are in the order as mentioned:
                # id, name, domain, year founded, industry, size range, locality, country, linkedin url, current employee estimate, total employee estimate
                
                # Adjust the indices to match your column structure
                Company.objects.create(
                    name=row[1],
                    domain=row[2],
                    year_founded=row[3],
                    industry=row[4],
                    size_range=row[5],
                    locality=row[6],
                    country=row[7],
                    linkedin_url=row[8],
                    current_employee_estimate=row[9],
                    total_employee_estimate=row[10]
                )
                
        logger.info(f"Finished processing the CSV file at: {file_path}")
    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")

    # Optionally, remove the file after processing to save storage space
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"Removed CSV file: {file_path}")