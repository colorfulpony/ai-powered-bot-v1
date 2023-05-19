import re

def remove_repeating_text(text):
    try:
        if not isinstance(text, str):
            raise TypeError("text argument must be a string")

        # Split the text into sentences
        sentences = text.split(". ")

        # Remove duplicate sentences
        unique_sentences = list(set(sentences))

        # Join the unique sentences into a single string
        output_text = ". ".join(unique_sentences)
        
        return output_text
    except Exception as error:
        print(f"An unexpected error occurred while removing duplicate: {error}")
