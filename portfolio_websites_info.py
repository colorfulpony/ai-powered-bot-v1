from get_portfolio_link import get_portfolio_link
from get_all_links import get_all_links
import requests
from analyze_portfolio_company import analyze_portfolio_company
from urllib.parse import urlparse

DELETE_URL_THAT_STARTS_WITH = ('https://b12.io', 'https://www.linkedin.com', 'https://vimeo.com', 'https://www.google.com', 'https://services', 'https://www.twitter.com', 'https://www.pingidentity.com', 'https://goo', 'https://www.facebook.com', 'https://instagram.com', 'https://www.crunchbase.com/', 'https://angel.co/', 'https://www.producthunt.com/', 'https://www.techcrunch.com/', 'https://www.forbes.com/', 'https://www.bloomberg.com/', 'https://www.reuters.com/', 'https://www.wsj.com/', 'https://www.nytimes.com/', 'https://www.cnbc.com/', 'https://www.barrons.com/', 'https://www.businessinsider.com/', 'https://www.inc.com/', 'https://www.fastcompany.com/', 'https://www.wired.com/', 'https://www.entrepreneur.com/', 'https://www.ycombinator.com/', 'https://500.co/', 'https://www.seedcamp.com/', 'https://www.accel.com/', 'https://www.greylock.com/', 'https://www.indexventures.com/', 'https://www.kleinerperkins.com/', 'https://www.greylock.com/', 'https://www.benchmark.com/', 'https://www.socialcapital.com/', 'https://www.softbank.com/', 'https://www.samsung.com/us/', 'https://www.qualcomm.com/', 'https://www.ibm.com/', 'https://www.microsoft.com/', 'https://aws.amazon.com/', 'https://www.google.com/', 'https://www.apple.com/', 'https://www.facebook.com/', 'https://www.twitter.com/', 'https://www.linkedin.com/', 'https://www.instagram.com/', 'https://www.youtube.com/', 'https://vimeo.com/', 'https://www.slideshare.net/', 'https://www.quora.com/', 'https://medium.com/', 'https://www.reddit.com/', 'https://www.stackoverflow.com/', 'https://www.github.com/', 'https://www.codepen.io/', 'https://dribbble.com/', 'https://www.behance.net/', 'https://www.figma.com/', 'https://www.invisionapp.com/', 'https://www.intercom.com/', 'https://www.mixpanel.com/', 'https://www.optimizely.com/', 'https://www.pingdom.com/', 'https://www.pingidentity.com/', 'https://www.cloudflare.com/', 'https://www.akamai.com/', 'https://www.salesforce.com/', 'https://www.hubspot.com/', 'https://www.marketo.com/', 'https://www.mailchimp.com/', 'https://www.zendesk.com/', 'https://www.atlassian.com/', 'https://slack.com/', 'https://www.dropbox.com/', 'https://www.box.com/', 'https://www.google.com/drive/', 'https://www.icloud.com/', 'https://trello.com/', 'https://www.notion.so/', 'https://www.asana.com/', 'https://www.todoist.com/', 'https://www.evernote.com/', 'https://www.nike.com/', 'https://www.adidas.com/', 'https://www.underarmour.com/', 'https://www.lululemon.com/', 'https://www.gap.com/', 'https://www.zara.com/', 'https://www.hm.com/', 'https://www.amazon.com/', 'https://www.walmart.com/', 'https://www.target.com/', 'https://www.bestbuy.com/', 'https://www.costco.com/', 'https://www.netflix.com/', 'https://www.hulu.com/', 'https://www.disneyplus.com/', 'https://www.primevideo.com/', 'https://www.hbo.com/', 'https://www.spotify.com/', 'https://www.apple.com/apple-music/',)

def get_portfolio_websites_info(website_url):
    try:
        portfolio_websites_data = []
        website_portfolio_link = get_portfolio_link(website_url)
        if website_portfolio_link:  
            portfolio_websites_data = get_portfolio_website_data(website_url, website_portfolio_link)   
        elif requests.get(website_url + '/portfolio').status_code == 200:
            portfolio_websites_data = get_portfolio_website_data(website_url, website_url + '/portfolio')
        elif requests.get(website_url + '/portfolios').status_code == 200:
            portfolio_websites_data = get_portfolio_website_data(website_url, website_url + '/portfolios')
        elif requests.get(website_url + '/companies').status_code == 200:
            portfolio_websites_data = get_portfolio_website_data(website_url, website_url + '/companies')
        elif requests.get(website_url + '/our-portfolio').status_code == 200:
            portfolio_websites_data = get_portfolio_website_data(website_url, website_url + '/our-portfolio')
        elif requests.get(website_url + '/ventures').status_code == 200:
            portfolio_websites_data = get_portfolio_website_data(website_url, website_url + '/ventures')
        elif requests.get(website_url + '/copy-of-portfolio').status_code == 200:
            portfolio_websites_data = get_portfolio_website_data(website_url, website_url + '/copy-of-portfolio')
        if portfolio_websites_data == None:
            return []
        else:
            return portfolio_websites_data
    except Exception as error:
        print(f"An unexpected error occurred while getting portfolio_websites_info: {error}")
        
def get_portfolio_website_data(website_url, website_portfolio_link):
    main_domain = urlparse(website_url).netloc
    portfolio_websites_data = []
    website_portfolio_links = get_all_links(website_portfolio_link)
    for portfolio_link in website_portfolio_links:
        website_portfolio_links = [link for link in website_portfolio_links if link.startswith("http://") or link.startswith("https://")]
        website_portfolio_links = [link for link in website_portfolio_links if not link.startswith('/')]
        website_portfolio_links = [link for link in website_portfolio_links if main_domain not in urlparse(link).netloc]
        website_portfolio_links = [link for link in website_portfolio_links if not link.startswith(DELETE_URL_THAT_STARTS_WITH)]
        website_portfolio_links = list(set(website_portfolio_links))
    website_portfolio_links = website_portfolio_links[:15]
    for website_portfolio_link in website_portfolio_links:
        website_portfolio_name, website_portfolio_solution, website_portfolio_url = analyze_portfolio_company(website_portfolio_link)
        if not website_portfolio_name.startswith("-") and not website_portfolio_solution.startswith("-"):
            portfolio_websites_data.append((website_portfolio_name, website_portfolio_solution, website_portfolio_url))
    return portfolio_websites_data