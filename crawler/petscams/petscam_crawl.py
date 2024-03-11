import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime
import json
import os
import time
from rate_calculate.calculator import calculate_success_rate


def is_broken_link(url):
    try:
        response = requests.get(url, timeout=10)
        if (response.status_code != 200 or "Account Suspended" in response.text or "This Account has been suspended" in response.text
                or "Future home of something quite cool" in response.text or "Sorry, we're doing some work on the site" in response.text
                or "Maintenance mode is on" in response.text or "The content is to be added" in response.text or "Index of /" in response.text
                or "Welcome to WordPress. This is your first post. Edit or delete it, then start writing!" in response.text):
            return True

    except requests.RequestException:
        return True
    return False


def save_broken_links(broken_links, filename='broken/websites1.json'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        json.dump(broken_links, file, indent=4)


def get_web(base_url, days=30, max_pages=40):
    current_date = datetime.datetime.now()
    scam_links = set() # Change to a set to avoid duplicates
    broken_links = []
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
                                if scam_url not in scam_links:  # Check if the URL is already in the set
                                    attempted_links += 1
                                if is_broken_link(scam_url):
                                    broken_links.append(scam_url)
                                else:
                                    scam_links.add(scam_url)
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

    return list(scam_links), attempted_links, broken_links


def save_url(scam_urls, filename='pet-scams1.json'):
    with open(filename, 'w') as file:
        json.dump(scam_urls, file, indent=4)


# Scrape and save the URLs in the Main function
def main():
    base_url = 'https://petscams.com/category/puppy-scammer-list/'
    scam_links, attempted_links, broken_links = get_web(base_url)
    save_broken_links(broken_links)
    valid_links = [link for link in scam_links if link not in broken_links]
    success_rate = calculate_success_rate("petscam_crawl", valid_links, attempted_links - len(broken_links))
    print(f"Success rate: {success_rate:.2f}%")
    save_url(valid_links)


if __name__ == "__main__":
    main()
