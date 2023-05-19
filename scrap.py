from playwright.sync_api import sync_playwright
import urllib.parse
from bs4 import BeautifulSoup
import logging
import random

logging.basicConfig(filename='scraping.log', level=logging.INFO)

with open('./user-agents.txt', 'r') as file:
    user_agents = file.read().splitlines()


def scrape(url: str) -> str:
    visited_urls = set()
    text = ""
    with sync_playwright() as p:
        try:
            user_agent = random.choice(user_agents)
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_extra_http_headers({"User-Agent": user_agent})
            text = scrape_main(page, url, visited_urls)
            browser.close()
        except Exception as e:
            logging.error(f"Error launching browser while main scraping: {e}")
    return text


def extract_text(page, url):
    try:
        page.goto(url, timeout=10000)
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        logging.info(f"Visited url: {url}")
        return text
    except Exception as e:
        logging.error(f"Error requesting while main scraping {url}: {e}")
        return ""


def scrape_main(page, start_url, visited_urls):
    text = ""
    visited_urls.add(start_url)
    text += extract_text(page, start_url)
    page.goto(start_url)
    soup = BeautifulSoup(page.content(), 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href or href.startswith("mailto:"):
            continue
        abs_url = urllib.parse.urljoin(start_url, href)
        logging.info(f"BEFORE ABS url: {abs_url}")

        if abs_url.startswith("http://"):
            abs_url = abs_url.replace("http://", "https://")

        if abs_url.startswith('/') or abs_url.startswith("#"):
            abs_url = urllib.parse.urljoin(start_url, abs_url)

        logging.info(f"ABS url: {abs_url}")
        if not abs_url.startswith(start_url) or not abs_url.startswith('https'):
            continue
        if abs_url in visited_urls:
            continue
        try:
            visited_urls.add(abs_url)
            text += scrape_subpages(page, abs_url)
        except Exception as e:
            logging.error(f"Error while main scraping {abs_url}: {e}")
    return text


def scrape_subpages(page, url):
    text = ""
    text += extract_text(page, url)
    return text


urls = [
    "https://www.9unicorns.in",
    "https://www.constructcap.com/",
    "https://continentalgrain.com/business/",
    "https://correlationvc.com/",
    "https://cosmicapital.com/",
    "https://www.cotacapital.com",
    "https://cptcap.com/",
    "https://www.creandum.com/",
    "https://cybernetix.vc",
    "https://cybernetix.vc",
]

if __name__ == "__main__":
    text = ""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in urls:
            text += scrape(url)
        browser.close()
    print(text)
