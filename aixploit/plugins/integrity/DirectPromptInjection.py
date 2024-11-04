import os
import logging
from ..base import Attacker
import yaml
from ...instrumentalize.ollama import prompt_ollama
from ...instrumentalize.openai import prompt_openai  
#logging.basicConfig(level=logging.DEBUG)  # Set the logging level
logging.basicConfig(level=logging.INFO)  # Set the logging level
LOGGER = logging.getLogger(__name__)  # Create a logger for this module


class PromptInjectorStandalone(Attacker):
    """
    This plugin is responsible for launching prompt injection attacks in a Standalone mode,
    no need to provide a prompt as input , just provide the URL and the API endpoint.
    This attack involves manipulating input data to change the intended behavior of a system.
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

        with open('attack_responses/scanoutput.txt', 'a') as output_file:  # {{ edit_4 }}
                # Process results (e.g., log or analyze)
            for prompt, response in self.results:  # {{ edit_5 }}
                output_file.write(f"prompt: {prompt}\nresponse: {response}\n@@@@@@@@@@@@@@@\n")  # Write to the file

        return self.results, True, 0.0


class SinglePromptInjectorStandalone(Attacker):
    """
    This plugin is responsible for launching a single prompt injection attack in a Standalone mode,
    no need to provide a prompt as input , just provide the URL and the API endpoint.
    This attack involves manipulating input data to change the intended behavior of a system.
    """
    def __init__(self, prompt: str):  # {{ edit_1 }}
        self.prompt = prompt  # Store the single prompt
        self.results = []  # Initialize results

    def run(self, url: str, provider: str, model: str, api_key: str) -> tuple[str, bool, float]:
        if url.strip() == "":
            return url, True, -1.0
        else:
            prompt_text = self.prompt.strip()  # Use the single prompt
            if provider.lower() == "ollama":  # Check if the API type is Ollama  {{ edit_7 }}
                response = prompt_ollama(url, model, prompt_text, api_key)
            else:
                # Handle other API types (e.g., OpenAI, Vertex) here
                response = "Unsupported API type" 
            self.results.append((prompt_text, response))

            with open('attack_responses/scanoutput.txt', 'a') as output_file:  # {{ edit_4 }}
                # Process results (e.g., log or analyze)
                for prompt, response in self.results:  # {{ edit_5 }}
                    output_file.write(f"prompt: {prompt}\nresponse: {response}\n@@@@@@@@@@@@@@@\n")  # Write to the file

            return self.results, True, 0.0
        

class PromptInjector(Attacker):
    """
    This plugin is responsible for launching prompt injection attacks in an integrated mode,
    you need to provide a prompt as input and the attack will be applied as an extension of 
    the input prompt. The source of attack is a YAML file that contains injection payloads.
    This attack involves manipulating input data to change the intended behavior of a system.
    """

    def __init__(self, prompt: str, payloadsource: str, source_type: str):  # {{ edit_1 }}
        self.results = [] # Initialize results
        self.prompt = prompt # Store the prompt that will be used as legitime request
        self.source = payloadsource # Store the payload source  
        self.source_type = source_type  # 'file' or 'db'
       

    def get_yaml_content(self):  # Helper method to load prompts from YAML
        if self.source_type == 'file':         
            with open(self.source, 'r') as file:
                data = yaml.safe_load(file)
                # Extract prompts and payloads
                return [
                {
                    'prompt': item['prompt'],
                    'payload': item.get('payload', '')  # Safely get payload, default to empty string
                }
                for item in data['prompt_injections']  # Iterate over each item in prompt_injections
            ]
        elif self.source_type == 'db':
            # Implement database extraction logic here
            # Example: return fetch_prompts_from_db(self.source)
            return []  # Placeholder for database prompts
        else:
            raise ValueError("Unsupported source type. Use 'file' or 'db'.")

    def get_yaml_payloads(self):  # Helper method to load payloads from YAML
        if self.source_type == 'file':         
            with open(self.source, 'r') as file:
                data = yaml.safe_load(file)
                # Extract only payloads from prompt_injections
                return [item.get('payload', '') for item in data.get('prompt_injections', [])]  # Safely access prompt_injections
        elif self.source_type == 'db':
            # Implement database extraction logic here
            # Example: return fetch_payloads_from_db(self.source)
            return []  # Placeholder for database payloads
        else:
            raise ValueError("Unsupported source type. Use 'file' or 'db'.")   

    def concat_prompts(self):  # {{ edit_3 }}
        prompts = [] 
        
        if self.prompt:  # Check if a prompt is provided
            for prompt_injection in self.get_yaml_content():  # Get prompts from YAML
                if isinstance(prompt_injection, dict):  # Ensure prompt_injection is a dictionary
                    concatenated_prompt = f"{self.prompt} {prompt_injection['prompt']}"  # Concatenate input prompt with each YAML prompt
                    prompts.append({'malicious_prompt': concatenated_prompt})  # Add the concatenated prompt

                else:
                    raise ValueError("Expected prompt_injection to be a dictionary.")  # Handle unexpected structure       
        return prompts
        
    def verify_success(self, payload: str, response: str, success_score: float, success_threshold: float = 0.5) -> bool:
        """
        Verifies if a prompt is succeeding based on the presence of the payload in the response
        and the risk score.

        Args:
            payload (str): The payload to check for in the response.
            response (str): The response generated by the prompt.
            success_score (float): The risk score associated with the prompt.
            success_threshold (float): The threshold below which the prompt is considered successful.

        Returns:
            bool: True if the prompt is considered successful, False otherwise.
        """
        # Check if the payload is in the response and the success score is below the success threshold
        #print(f"Payload type: {type(payload)}, Response type: {type(response)}, Success Score: {success_score}")
        #print(f"Payload: '{payload}', Response: '{response}'")
        
        if payload.strip() and payload.strip().lower() in response.strip().lower() :
            return True
        return False

    def run(self, provider: str, url: str,  model: str, api_key: str, verbose: bool = False) -> tuple[str, bool, float]:
        attack_success = False
        provider = provider.strip()  # Ensure no leading/trailing spaces
        model = model.strip()  # Ensure no leading/trailing spaces
        api_key = api_key.strip()  # Ensure no leading/trailing spaces
        if url.strip() == "" and provider.lower() != "openai":
            return url, True, -1.0
        else:
            prompts = self.concat_prompts()
            payloads = self.get_yaml_payloads()
            total_prompts = len(prompts)
            successful_prompts = 0  # Counter for successful prompts
  # {{ edit_3 }}
    # Pl
    # ay each prompt on the specified URL
        for prompt, payload in zip(prompts, payloads):
            malicious_prompt = prompt['malicious_prompt'].strip()
            malicious_payload = payload.strip()
             # Ensure no leading/trailing spaces

            provider_functions = {  # {{ edit_7 }}
                "ollama": lambda: prompt_ollama(url, model, malicious_prompt, api_key),
                "openai": lambda: prompt_openai(url, model, malicious_prompt, api_key )  # Ensure parameters are correct
            }

            # Get the response using the provider functions or handle unsupported API types
            try:
                response = provider_functions.get(provider.lower(), lambda: "Default Unsupported API type")()  # Call the corresponding function or return default
                #LOGGER.info(f"Calling provider with parameters: provider={provider}, model={model}, prompt={malicious_prompt}, api_key={api_key}")
                attack_success = self.verify_success(malicious_payload, response, 1.0)
                if attack_success:
                    successful_prompts += 1
                    #LOGGER.info("Attack succeded")
                else:
                    #LOGGER.info("Attack failed")
                    pass
            except Exception as e:
                response = "Error during API call"
                #LOGGER.error(f"API call to {provider} with parameters: url={url}, model={model}, prompt={malicious_prompt}, api_key={api_key} failed: {e}")  # Log the error
            # Further processing of the response can be done here
                
                 # Log failure

            #print(f"Response content: {response}") 
            self.results.append((malicious_prompt, response))
        success_rate = successful_prompts / total_prompts if total_prompts > 0 else 0.0

        with open('attack_responses/scanoutput.txt', 'a') as output_file:  # {{ edit_4 }}
                # Process results (e.g., log or analyze)
            for prompt, response in self.results:  # {{ edit_5 }}
                output_file.write(f"prompt: {prompt}\nresponse: {response}\n@@@@@@@@@@@@@@@\n")  # Write to the file
        
        #LOGGER.info("Attack completed with a success rate of %s", success_rate)
        return self.results, attack_success, success_rate



class SinglePromptInjector(Attacker):
    """
    This plugin is responsible for launching prompt injection attacks in an integrated mode,
    you need to provide a prompt as input and and an attack payload as input,  the attack will be applied as an extension of 
    the input prompt. 
    """
    def __init__(self,prompt: str, payload: str):  # {{ edit_1 }}
        self.results = []
        self.attack_prompt = payload
        self.prompt = prompt

    def concat_prompts(self):  # {{ edit_3 }}
        concatenated_prompt = f"{self.prompt} {self.attack_prompt}"  # Concatenate input prompt with the payload
        return concatenated_prompt 
        
    def verify_success(self, payload: str, response: str, success_score: float, success_threshold: float = 0.5) -> bool:
        """
        Verifies if a prompt is succeeding based on the presence of the payload in the response
        and the risk score.

        Args:
            payload (str): The payload to check for in the response.
            response (str): The response generated by the prompt.
            success_score (float): The risk score associated with the prompt.
            success_threshold (float): The threshold below which the prompt is considered successful.

        Returns:
            bool: True if the prompt is considered successful, False otherwise.
        """
        # Check if the payload is in the response and the success score is below the success threshold
        #print(f"Payload type: {type(payload)}, Response type: {type(response)}, Success Score: {success_score}")
        #print(f"Payload: '{payload}', Response: '{response}'")
        
        if payload.strip() and payload.strip().lower() in response.strip().lower() :
            return True
        return False

    def run(self, provider: str, url: str,  model: str, api_key: str, verbose: bool = False) -> tuple[str, bool, float]:
        attack_success = False
        provider = provider.strip()  # Ensure no leading/trailing spaces
        model = model.strip()  # Ensure no leading/trailing spaces
        api_key = api_key.strip()  # Ensure no leading/trailing spaces
        if url.strip() == "" and provider.lower() != "openai":
            return url, True, -1.0
        else:
            malicious_prompt = self.concat_prompts()
            successful_prompts = 0  # Counter for successful prompts
  # {{ edit_3 }}
    # Pl
    # ay each prompt on the specified URL


             # Ensure no leading/trailing spaces

        provider_functions = {  # {{ edit_7 }}
            "ollama": lambda: prompt_ollama(url, model, malicious_prompt, api_key),
            "openai": lambda: prompt_openai(url, model, malicious_prompt, api_key )  # Ensure parameters are correct
        }

        # Get the response using the provider functions or handle unsupported API types
        try:
            response = provider_functions.get(provider.lower(), lambda: "Default Unsupported API type")()  # Call the corresponding function or return default
            #LOGGER.info(f"Calling provider with parameters: provider={provider}, model={model}, prompt={malicious_prompt}, api_key={api_key}")
            attack_success = self.verify_success(self.attack_prompt, response, 1.0)
            LOGGER.info(f"Calling provider with parameters: provider={self.attack_prompt}")
            if attack_success:
                successful_prompts += 1
                LOGGER.info("Attack succeded")
            else:
                LOGGER.info("Attack failed")
                pass
        except Exception as e:
            response = "Error during API call"
            #LOGGER.error(f"API call to {provider} with parameters: url={url}, model={model}, prompt={malicious_prompt}, api_key={api_key} failed: {e}")  # Log the error
        # Further processing of the response can be done here
            
                # Log failure

        #print(f"Response content: {response}") 
        self.results.append((malicious_prompt, response))
        success_rate = successful_prompts / 1 if 1 > 0 else 0.0

        with open('attack_responses/scanoutput.txt', 'a') as output_file:  # {{ edit_4 }}
                # Process results (e.g., log or analyze)
            for prompt, response in self.results:  # {{ edit_5 }}
                output_file.write(f"prompt: {prompt}\nresponse: {response}\n@@@@@@@@@@@@@@@\n")  # Write to the file
        
        #LOGGER.info("Attack completed with a success rate of %s", success_rate)
        return self.results, attack_success, success_rate