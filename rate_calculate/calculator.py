import datetime
import os
import time
import json

from secret import RATE_RESULT_FILE

rate_results_file = RATE_RESULT_FILE


def calculate_success_rate(crawler_name, scraped_links, attempted_links, start_time):
    if attempted_links == 0:
        return 0  # avoid division by zero
    else:
        success_rate = (len(scraped_links) / attempted_links) * 100

    if not os.path.exists(rate_results_file):
        rate_results = {}
    else:
        with open(rate_results_file, 'r') as file:
            rate_results = json.load(file)

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%b %d at %H:%M')

    crawl_id = f"{crawler_name}_{timestamp.replace(' ', '_').replace(':', '')}"

    # Record the result for this specific crawl
    rate_results[crawl_id] = {
        "start_time": start_time,
        "end_time": timestamp,
        "success_rate": success_rate,
        "scraped_links": len(scraped_links),
        "attempted_links": attempted_links
    }

    with open(rate_results_file, 'w') as file:
        json.dump(rate_results, file, indent=4)

    return success_rate
