from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import urlparse, urljoin

def get_all_links(url: str) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url)
        except Exception as e:
            print(f"Error navigating to {url}, get_all_links: {e}")
            return []
        
        links = page.query_selector_all("a")
        hrefs = [link.get_attribute("href") for link in links]
        absolute_hrefs = [urljoin(url, href) for href in hrefs if href and urlparse(href).scheme in ["http", "https"]]
        return absolute_hrefs
