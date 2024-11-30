from openai import OpenAI  # Ensure you have the OpenAI library installed

import tiktoken  # Import the tiktoken library


def prompt_openai(
    url: str, model: str, prompt_text: str, api_key: str
) -> str:  # Function to send a prompt to the Ollama API
    # Initialize the OpenAI client with the Ollama API base URL
    client = OpenAI(  # OpenaI API base URL
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


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    # https://openai.com/api/pricing/
    if model == "gpt-4o-mini":
        price_per_prompt_tokens = 250 / 10000000
        price_per_completion_tokens = 250 / 10000000
    else:
        price_per_prompt_tokens = 100 / 10000000
        price_per_completion_tokens = 100 / 10000000
    # Example cost per token for the OpenAI API
    return (
        prompt_tokens * price_per_prompt_tokens,
        completion_tokens * price_per_completion_tokens,
    )
