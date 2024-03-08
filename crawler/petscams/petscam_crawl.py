import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime
import json
import time
from rate_calculate.calculator import calculate_success_rate


def get_web(base_url, days=3, max_pages=4):
    current_date = datetime.datetime.now()
    scam_links = []
    page_url = base_url
    page_count = 0
    attempted_links = 0

    with requests.Session() as session:
        while page_url and page_count < max_pages:
            print(f"Fetching {page_url}...")
            response = session.get(page_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.find_all('article')
            for article in articles:
                try:
                    time_tag = article.find('time')
                    if time_tag:
                        date_text = time_tag.get_text()
                        article_date = datetime.datetime.strptime(date_text, '%B %d, %Y')

                        if (current_date - article_date).days <= days:
                            title_tag = article.find('h1', class_='main-title')
                            if title_tag:
                                scam_url = title_tag.get_text().strip()
                                if not scam_url.startswith('http'):
                                    scam_url = 'https://' + scam_url
                                attempted_links += 1
                                scam_links.append(scam_url)
                except Exception as e:
                    print(f"An error occurred: {e}")

            next_link = soup.find('a', string=lambda x: x and 'next' in x.lower())
            if next_link and next_link.get('href'):
                page_url = urljoin(base_url, next_link['href'])
                page_count += 1
                time.sleep(2)
            else:
                page_url = None
            print("Fetching complete.")

    return scam_links, attempted_links


def save_url(scam_urls, filename='pet-scams.json'):
    with open(filename, 'w') as file:
        json.dump(scam_urls, file, indent=4)


# Scrape and save the URLs in the Main function
def main():
    base_url = 'https://petscams.com'
    scam_links, attempted_links = get_web(base_url)
    success_rate = calculate_success_rate("petscam_crawl", scam_links, attempted_links)
    print(f"Success rate: {success_rate:.2f}%")
    save_url(scam_links)


if __name__ == "__main__":
    main()
