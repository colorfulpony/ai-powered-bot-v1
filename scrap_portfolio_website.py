from playwright.sync_api import Playwright, sync_playwright

def scrap_portfolio_website(url: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(url)
            text = page.inner_text('body')
        except Exception as e:
            text = f"Error occurred while scrapping portfolio website: {str(e)}"
        finally:
            browser.close()
        return text
