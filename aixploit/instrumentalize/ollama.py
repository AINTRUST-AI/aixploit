
from openai import OpenAI  # Ensure you have the OpenAI library installed

def prompt_ollama(url: str, model:str, prompt_text: str, api_key: str ) -> str:  # Function to send a prompt to the Ollama API
    # Initialize the OpenAI client with the Ollama API base URL
    client = OpenAI(
        base_url=url.strip(),  # Ollama API base URL
        api_key=api_key.strip(),  # Use the provided API key
    )
    response = client.chat.completions.create(
        model=model,  # Specify the model to use
        messages=[
            # {"role": "system", "content": "You are a chatbot"},  # Not useful for now
            {"role": "user", "content": prompt_text},  # User prompt
        ]
    )
    result = ''
    for choice in response.choices:  # Iterate through the response choices
        result += choice.message.content  # Concatenate the content of each choice

    return result  # Return the concatenated result