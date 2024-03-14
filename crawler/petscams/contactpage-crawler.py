import json
import os
import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from rate_calculate.calculator import calculate_success_rate


# Heuristic Approach : match form pages based on a set of predefined keywords
def find_contact_form(soup):
    for form in soup.find_all('form'):
        if form.find('input', {'type': 'text'}) and form.find('input', {'type': 'email'}) and form.find('textarea'):
            return form
    return None


def get_contact_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # First try to find a contact form directly on the page
        form = find_contact_form(soup)
        if form:
            return url

        # If no form is found, fall back to heuristic search for contact pages
        contact_keywords = ['contact-us', 'contact', 'reach-us', 'get-in-touch', 'enquire now', 'show-now',
                            'reach out to us']
        for keyword in contact_keywords:
            contact_link = soup.find('a', href=lambda href: href and keyword in href.lower())
            if contact_link:
                return urljoin(url, contact_link['href'])

        # Look for an 'a' element with the keyword in its text inside 'li' elements
        list_items = soup.find_all('li')
        for li in list_items:
            a_tag = li.find('a')
            if a_tag and a_tag.string and any(keyword in a_tag.string.lower() for keyword in contact_keywords):
                return urljoin(url, a_tag['href'])

    except requests.RequestException as e:
        print(f"An error occurred while requesting {url}: {e}")
    return None


def read_urls(filename='pet-scams1.json'):
    with open(filename, 'r') as file:
        return json.load(file)


def save_urls(scam_urls, success_filename, fail_filename):
    success_path = os.path.join('success', success_filename)
    fail_path = os.path.join('fail', fail_filename)

    os.makedirs(os.path.dirname(success_path), exist_ok=True)
    os.makedirs(os.path.dirname(fail_path), exist_ok=True)

    with open(success_path, 'w') as file:
        json.dump(scam_urls['success'], file, indent=4)

    with open(fail_path, 'w') as file:
        json.dump(scam_urls['fail'], file, indent=4)


def main():
    start_time = int(time.time())
    urls = read_urls()
    results = {'success': [], 'fail': []}
    attempted_links = 0

    for url in urls:
        attempted_links += 1
        contact_url = get_contact_page(url)
        if contact_url:
            results['success'].append(contact_url)
        else:
            results['fail'].append(url)
            print(f"Contact page not found for {url}")

    save_urls(results, 'contact-page1.json', 'contact-page1.json')
    success_rate = calculate_success_rate('contactpage_crawl', results['success'], attempted_links, start_time)
    print(f"Success rate: {success_rate:.2f}%")


if __name__ == "__main__":
    main()
