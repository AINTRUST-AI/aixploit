from openai import OpenAI  # Ensure you have the OpenAI library installed
import tiktoken


def prompt_ollama(
    url: str, model: str, prompt_text: str, api_key: str
) -> str:  # Function to send a prompt to the Ollama API
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
        ],
    )
    result = ""
    for choice in response.choices:  # Iterate through the response choices
        result += choice.message.content  # Concatenate the content of each choice

    return result  # Return the concatenated result


def count_tokens(prompt, response):
    # Initialize the tokenizer for the specific model you are using
    # For example, for the 'gpt-3.5-turbo' model:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    prompt_tokens = len(tokenizer.encode(prompt))

    completion_tokens = len(tokenizer.encode(response))
    total_tokens = prompt_tokens + completion_tokens  # Total tokens used in the call

    return prompt_tokens, completion_tokens, total_tokens
