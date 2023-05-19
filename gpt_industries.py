import os
import openai
import time
import sys
import traceback
import random
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (openai.error.RateLimitError,),
):
    """Retry a function with exponential backoff."""
 
    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay
 
        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)
 
            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1
 
                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )
 
                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())
 
                # Sleep for the delay
                time.sleep(delay)
 
            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e
 
    return wrapper


# @retry_with_exponential_backoff
def gpt_get_industries(text):
    context = """You are a very good analyst of investment companies. 
    Answer the task based on the context below. Keep the answer only in the format I have written below and not in any other format. Just write "-" and nothing else if you not sure about the answer or if there is no info about the industries at all. Don't ask questions. Don't write anything else. Don't write your explanations.
Task: Analyze the context given to you at the very end and find the industries in which this investment fund invests. Use only those industries that I wrote below."

Desired answer format:
<comma_separated_list_of_company_ivesting_industries>

Example of desired answer format:
AI, Biotech, Healthcare

Comma separated list of all investment industries: Technology, E-commerce, Healthcare, Finance, Education, Food, Beverage, Energy, Travel, Hospitality, Real Estate, Entertainment, Social Impact, Marketing, Advertising, Transportation, Logistics, Manufacturing, Agriculture, Fashion, Beauty, Personal Care, Fitness, Wellness, Home Services, Construction, Engineering, Automotive, Sports, Recreation, Art, Design, Media, Publishing, Government, Public Services, Professional Services, HR, Recruitment, Gaming, Esports, Insurance, Telecommunications, Security, Surveillance, Aerospace, Defense, Biotechnology, Pharmaceuticals, Chemicals, Consumer Electronics, Consumer Goods, Environmental Services, Hospitality, Events, Industrial Automation, Robotics, Legal Services, Materials Science, Medical Devices, Mining, Metals, Nanotechnology, Packaging, Containers, Plastics, Rubber, Retail, Social Media, Networking, Software, IT Services, Supply Chain, Logistics, Virtual, Augmented Reality, Crowdfunding, Fundraising, Internet of Things, Smart Homes, Robotics, Drones, AI, Machine Learning, Blockchain, Cryptocurrency, Quantum Computing, Space Exploration, Commercialization, Urban Farming, Agriculture, Waste Management, Recycling, Water, Waste Treatment, 3D Printing, Additive Manufacturing, Architecture, Design, Cloud Computing, Databases, Information Management, Design, User Experience, Digital Signage, Display Advertising,DTC Products, Distributed Ledger Technology, Document Management, Automation, Employee Benefits, Perks, Event Planning, Management, Facility Management, Maintenance, Financial Technology, Services, Fleet Management, Transportation Services, Food Delivery, Meal Kits, Health, Fitness Wearables, Home Security, Surveillance, Identity, Access Management, Influencer Marketing, Social Media Advertising, Intellectual Property Management, Internet Services, ISPs, Legal Tech, Services, Logistics, Supply Chain Management, Marketing Automation, Analytics, Medical Research, Development, Online Learning Platforms, MOOCs, Online Marketplaces, Auctions, Personalized Nutrition, Wellness, Privacy, Data Security, Procurement, Vendor Management, Product Design, Development, Professional Development, Training, Property Management, Maintenance, Public Relations, Communications, Renewable Energy, Clean Tech, Smart City, Infrastructure, Wearable Technology, IoT Devices, Advanced Materials, Agritech, Air Quality Control, Animal Health, Nutrition, App Development, Design, Asset Management, Investment, Audio, Music, Autonomous Vehicles, Behavioral Analytics, Insights, Big Data, Analytics, Bioinformatics, Genomics, Business Intelligence, Analytics, Cloud Services, Infrastructure, Cognitive Computing, AI, Collaborative Tools, Workspaces, Commercial Real Estate, Communication, Networking, Computer Vision, Image Processing, Construction Tech, Building Materials, Corporate Social Responsibility,CRM, Cybersecurity, Privacy, Data Science, Analysis, Defense, Security, Digital Currency, Payments, Digital Marketing, Advertising, Digital Rights Management, Disaster Response, Relief, Diversity, Equity,, Inclusion (DEI), Document Collaboration, Sharing, Drones, Unmanned Aerial Vehicles (UAVs), E-commerce Platforms, Marketplaces, Education Technology, Services, Electric Vehicles, Charging Infrastructure, Electronic Components, Devices, Emerging Technologies, Innovation, Employee Engagement, Retention, Energy Storage, Distribution, Enterprise Resource Planning (ERP), Environmental Monitoring, Assessment, Event Ticketing, Management, Facility Maintenance, Management, Fashion Technology, Wearables, Financial Planning, Management, Fleet Maintenance, Management, Food Science, Technology, Fraud Detection, Prevention, Gaming, Gamification, Geo-location Services, Analytics, Graphic Design, Animation."""

    prompt_template = """Context: {}"""

    # Split text into smaller chunks with a maximum length of 4096 tokens
    text_chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]

    # Initialize the messages list with the context
    messages = [{"role": "system", "content": context}]

    # Loop through the text chunks and generate prompts for each one
    for i, chunk in enumerate(text_chunks):

        prompt = prompt_template.format(chunk)

        messages.append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        chat_response = completion.choices[0].message.content

        # Only include the answer from the last chunk
        if i == len(text_chunks) - 1:
            messages.append({"role": "system", "content": chat_response})
        return chat_response
    return chat_response
        
