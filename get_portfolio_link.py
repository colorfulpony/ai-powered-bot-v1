import requests
from bs4 import BeautifulSoup

desired_titles = ['How We Invest', 'Portfolio', 'Investments', 'Our Investments', 'Companies', 'Ventures', 'VC', "Our Portfolio", "Investments", "Our Investments", "Portfolio", "Our Portfolio", "Startup Portfolio", "Investment Portfolio", "Companies", "Startup Companies", "Invested Companies", "Our Companies", "Portfolio Companies", "Funded Startups", "Startup Investments", "Investment List", "Startup List", "Funded Companies", "Our Startups", "Our Investments in Startups", "Companies We've Invested In", "Our Startup Portfolio", "Our Venture Portfolio", "Our Investment Portfolio in Startups", "Startup Ventures", "Portfolio of Funded Startups", "Venture Investments", "Our Investment List in Startups", "Our Startup Investments", "Startups We've Funded", "Our Startup Fund", "Our Funded Ventures", "Our Venture Capital Portfolio", "Our Seed Investments", "Our Angel Investments", "Our Startup Ecosystem", "Our Innovation Portfolio", "Our Accelerator Portfolio", "Our Incubator Portfolio", "Our Startup Studio Portfolio", "Our Seed Fund Portfolio", "Our Angel Investment Portfolio", "Our Early-Stage Investments", "Our Growth-Stage Investments", "Our Startup Partners", "Our Innovation Partners", "Our Startup Network", "Our Startup Community", "Our Startup Ecosystem Investments", "Our Technology Investments", "Our AI Portfolio", "Our Blockchain Portfolio", "Our Fintech Portfolio", "Our Healthtech Portfolio", "Our Edtech Portfolio", "Our Retailtech Portfolio", "Our SaaS Portfolio", "Our Enterprise Portfolio", "Our Mobile Portfolio", "Our Social Impact Portfolio"]

tags = ['nav', 'div', 'header']

classes = ['navbar', 'main-nav', 'header-nav', 'nav', 'site-nav', 'hamburger', 'nav-item', 'menu-item', 'menu-link', 'nav-link', 'portfolio-link', 'investment-link', 'startups-link', 'companies-link', 'portfolio-nav', 'investment-nav', 'startups-nav', 'companies-nav', 'main-nav', 'header-nav', 'site-nav', 'primary-nav', 'secondary-nav', 'utility-nav', 'mega-nav', 'hamburger', 'menu-toggle', 'nav-toggle', 'nav-icon', 'nav-button', 'nav-bar', 'nav-menu', 'nav-dropdown', 'nav-list', 'sub-nav', 'breadcrumb-nav', 'footer-nav', 'menu']

def get_portfolio_link(url):
    try:
        href = ""
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        nav_links = []
        navbar = None

        # Find the navigation bar by looking for a container element with a consistent class or ID
        possible_containers = soup.find_all(tags, class_=classes) or \
        soup.find_all('nav') or \
        soup.find_all('header')
                            
        if possible_containers:
            for container in possible_containers:
                # Check if the container contains any links with the desired titles
                links = container.find_all('a', string=lambda s: s and any(title in s for title in desired_titles))
                if links:
                    navbar = container
                    break

        # If we found the navbar, extract the links with the desired titles
        if navbar:
            for link in navbar.find_all('a', string=lambda s: s and any(title in s for title in desired_titles)):
                href = link.get('href')
            
            if href.startswith('/') or href.startswith("#"):
                href = url + href[1:]       
        else:
            print(f"No navbar found on {url}")
        return href
    except requests.exceptions.RequestException as e:
        print("Error while getting portfolio link: Failed to retrieve website content. Exception:", e)
    except Exception as e:
        print("Error while getting portfolio link:", e)
    
    
