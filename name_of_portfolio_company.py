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
def get_name_of_portfolio_company(text):
    context = """You are a very good analyst of startups. 
    Answer the task based on the context below. Keep the answer only in the format I have written below and not in any other format. Just write "-" and nothing else if you not sure about the answer or if there is no info about the name at all. Don't ask questions. Don't write anything else. Don't write your explanations.
Task: Analyze the context given to you at the very end and give me the name of the startup described in the context. Don't come up with any unreal names. I need only the real name based on the context
"""

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
    if chat_response.startswith('-') or chat_response.startswith("-"):
        chat_response = '-'
    return chat_response
        
