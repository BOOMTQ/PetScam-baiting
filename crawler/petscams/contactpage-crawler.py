import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Heuristic Approach : match form pages based on a set of predefined keywords
def get_contact_page(urls):
    contact_keywords = ['contact-us', 'contact', 'reach-us', 'get-in-touch']
    try:
        response = requests.get(urls)
        soup = BeautifulSoup(response.text, 'html.parser')
        for keyword in contact_keywords:
            contact_link = soup.find('a', href=lambda href: href and keyword in href.lower())
            if contact_link:
                return urljoin(urls, contact_link['href'])
    except requests.RequestException as e:
        print(f"An error occurred while requesting {urls}: {e}")
    return None


def read_urls(filename='pet-scams.json'):
    with open(filename, 'r') as file:
        return json.load(file)


def save_urls(scam_urls, filename='contact-page.json'):
    with open(filename, 'w') as file:
        json.dump(scam_urls, file, indent=4)


def main():
    urls = read_urls()
    contact_page_urls = []

    for url in urls:
        contact_url = get_contact_page(url)
        if contact_url:
            contact_page_urls.append(contact_url)
            save_urls(contact_page_urls)
        else:
            print(f"Contact page not found for {url}")


if __name__ == "__main__":
    main()
