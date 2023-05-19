from scrap import scrape
from remove_duplicate import remove_repeating_text
from gpt_stages import gpt_get_stages

def get_vc_stages(url):
    try:
        if not isinstance(url, str):
            raise TypeError("URL must be a string")
        
        text = scrape(url)
        if not isinstance(text, str):
            raise ValueError("Scraped text must be a string")
        
        non_repeat_text = remove_repeating_text(text)
        if not isinstance(non_repeat_text, str):
            raise ValueError("Non-repeated text must be a string")
        
        stages = gpt_get_stages(non_repeat_text)
        if not isinstance(stages, str):
            raise ValueError("GPT stages must be a string")
        
        return stages
    
    except Exception as e:
        print("An error occurred:", e)
