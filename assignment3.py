import argparse
import urllib.request
import csv
from collections import defaultdict
from datetime import datetime
import re


def downloadData(url):
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
    return data


def processData(data):
    csv_data = csv.reader(data.splitlines())

    total_requests = 0
    image_requests = 0
    browser_counter = defaultdict(int)
    hourly_requests = defaultdict(int)

    image_extensions_regex = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)


    firefox_regex = re.compile(r'Firefox', re.IGNORECASE)
    chrome_regex = re.compile(r'Chrome', re.IGNORECASE)
    safari_regex = re.compile(r'Safari', re.IGNORECASE)
    ie_regex = re.compile(r'Internet Explorer', re.IGNORECASE)


    for row in csv_data:
        path_to_file = row[0]
        datetime_accessed = row[1]
        browser = row[2]

        if image_extensions_regex.search(path_to_file):
            image_requests += 1


        if firefox_regex.search(browser):
            browser_counter['Firefox'] += 1
        elif chrome_regex.search(browser):
            browser_counter['Chrome'] += 1
        elif safari_regex.search(browser):
            browser_counter['Safari'] += 1
        elif ie_regex.search(browser):
            browser_counter['Internet Explorer'] += 1


        datetime_obj = datetime.strptime(datetime_accessed, "%Y-%m-%d %H:%M:%S")
        hour = datetime_obj.hour
        hourly_requests[hour] += 1

        total_requests += 1


    image_percentage = (image_requests / total_requests) * 100 if total_requests > 0 else 0
    print(f"Image requests account for {image_percentage:.1f}% of all requests")


    most_popular_browser = max(browser_counter, key=browser_counter.get)
    print(f"The most popular browser is {most_popular_browser}")


    for hour in range(24):
        print(f"Hour {hour:02} has {hourly_requests[hour]} hits")


def main(url):
    print(f"Running main with URL = {url}...")
    # Download the data from the provided URL
    downloaded_data = downloadData(url)

    # Process the downloaded data
    processData(downloaded_data)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
