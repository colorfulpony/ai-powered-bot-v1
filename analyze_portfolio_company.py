from scrap_portfolio_website import scrap_portfolio_website
from remove_duplicate import remove_repeating_text
from solution_of_portfolio_company import get_solution_of_portfolio_company
from name_of_portfolio_company import get_name_of_portfolio_company

def analyze_portfolio_company(url):
    try:
        website_portfolio_name = "-"
        website_portfolio_solution = "-"
        website_text = scrap_portfolio_website(url)
        if website_text:
            website_text = remove_repeating_text(website_text)
        if website_text:
            website_portfolio_name = get_name_of_portfolio_company(website_text)
        if website_text:
            website_portfolio_solution = get_solution_of_portfolio_company(website_text)

        
        return website_portfolio_name, website_portfolio_solution, url
    except Exception as error:
        print(f"An unexpected error occurred while analyzing_portfolio_company: {error}")