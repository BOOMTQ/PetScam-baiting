import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from rate_calculate.calculator import calculate_success_rate


# Heuristic Approach : match form pages based on a set of predefined keywords
# def get_contact_page(urls):
#     contact_keywords = ['contact-us', 'contact', 'reach-us', 'get-in-touch']
#     try:
#         response = requests.get(urls)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         for keyword in contact_keywords:
#             contact_link = soup.find('a', href=lambda href: href and keyword in href.lower())
#             if contact_link:
#                 return urljoin(urls, contact_link['href'])
#     except requests.RequestException as e:
#         print(f"An error occurred while requesting {urls}: {e}")
#     return None

def find_contact_form(soup):
    for form in soup.find_all('form'):
        if form.find('input', {'type': 'text'}):
            return form
    return None


def get_contact_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # First try to find a contact form directly on the page
        form = find_contact_form(soup)
        if form:
            return url  # Or return form['action'] if form has an action attribute

        # If no form is found, fall back to heuristic search for contact pages
        contact_keywords = ['contact-us', 'contact', 'reach-us', 'get-in-touch', 'show-now']
        for keyword in contact_keywords:
            contact_link = soup.find('a', href=lambda href: href and keyword in href.lower())
            if contact_link:
                return urljoin(url, contact_link['href'])

    except requests.RequestException as e:
        print(f"An error occurred while requesting {url}: {e}")
    return None


def read_urls(filename='pet-scams1.json'):
    with open(filename, 'r') as file:
        return json.load(file)


def save_urls(scam_urls, filename='contact-page1.json'):
    with open(filename, 'w') as file:
        json.dump(scam_urls, file, indent=4)


def main():
    urls = read_urls()
    contact_page_urls = []
    attempted_links = 0

    for url in urls:
        attempted_links += 1
        contact_url = get_contact_page(url)
        if contact_url:
            contact_page_urls.append(contact_url)
        else:
            print(f"Contact page not found for {url}")

    save_urls(contact_page_urls)
    success_rate = calculate_success_rate('contactpage_crawl', contact_page_urls, attempted_links)
    print(f"Success rate: {success_rate:.2f}%")


if __name__ == "__main__":
    main()
