import os
import logging
from ..base import Attacker
import yaml
from ...instrumentalize.ollama import prompt_ollama

#logging.basicConfig(level=logging.DEBUG)  # Set the logging level
#LOGGER = logging.getLogger(__name__)  # Create a logger for this module

class TokenFlooder(Attacker):
    """
    This plugin is designed to consume as many resources as possible, 
    with the goal of causing a denial-of-service (DoS) situation for an AI model.
    """
    results = []
    def __init__(self, source: str, source_type: str ):  # {{ edit_1 }}
        self.source = source
        self.source_type = source_type  # 'file' or 'db'
        pass

    def load_prompts(self):  # {{ edit_3 }}
        if self.source_type == 'file':
            
            with open(self.source, 'r') as file:
                data = yaml.safe_load(file)
                return data['prompt_injections']
        elif self.source_type == 'db':
            # Implement database extraction logic here
            # Example: return fetch_prompts_from_db(self.source)
            return []  # Placeholder for database prompts
        else:
            raise ValueError("Unsupported source type. Use 'file' or 'db'.")
        
    def run(self, url: str, provider: str, model: str, api_key: str) -> tuple[str, bool, float]:
        if url.strip() == "":
            return url, True, -1.0
        else:
            prompts = self.load_prompts()   # {{ edit_3 }}
    # Play each prompt on the specified URL
        for prompt in prompts:
            prompt_text = prompt['prompt'].strip() 
            if provider.lower() == "ollama":  # Check if the API type is Ollama  {{ edit_7 }}
                response = prompt_ollama(url, model, prompt_text, api_key)
            else:
                # Handle other API types (e.g., OpenAI, Vertex) here
                response = "Unsupported API type" 
            #print(f"Response content: {response}") 
            self.results.append((prompt_text, response))

        with open('attack_results/scanoutput.txt', 'w') as output_file:  # {{ edit_4 }}
                # Process results (e.g., log or analyze)
            for prompt, response in self.results:  # {{ edit_5 }}
                output_file.write(f"prompt: {prompt}\nresponse: {response}\n@@@@@@@@@@@@@@@\n")  # Write to the file

        return self.results, True, 0.0


