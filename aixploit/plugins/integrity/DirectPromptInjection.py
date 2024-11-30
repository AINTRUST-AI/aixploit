import os, sys
import logging
from ..base import Attacker
import yaml
import uuid  # Import the uuid module
from ...instrumentalize.validation import validation_prompt_openai
from datetime import datetime  # Make sure to import datetime at the top of your file

from ...instrumentalize.ollama import prompt_ollama
from ...instrumentalize.openai import prompt_openai, count_tokens, calculate_cost
#logging.basicConfig(level=logging.DEBUG)  # Set the logging level
logging.basicConfig(level=logging.INFO)  # Set the logging level
LOGGER = logging.getLogger(__name__)  # Create a logger for this module



class PromptInjection(Attacker):
    """
    This plugin is responsible for launching prompt injection attacks in a standalone mode,
    you need to provide a scan type as input and the attacker will load a corresponding YAML file 
    that contains malicious prompt  .
    This attack involves manipulating input data to change the intended behavior of a system.
    """

    def __init__(self, scan_type: str):  # {{ edit_1 }}
        self.results = [] # Initialize results as an empty list
        self.successful_prompt_injections = []  # Store the successfull promptinjection source 
        self.total_tokens = 0 # Initialize total tokens
        self.total_cost = 0.0 # Initialize total cost   
        self.scan_type = scan_type # 'file' or 'db'
       

    def get_prompts(self):  # Helper method to load prompts from YAML    
        try:   
            if self.scan_type.lower() == 'quick':

                source = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')), 'attack_prompts/quick_scan_payloads.yaml')
                with open(source, 'r') as file:
                    data = yaml.safe_load(file)
                # Extract prompts and payloads
                return [item.get('prompt', '') for item in data.get('prompt_injections', []) if 'prompt' in item] # Join prompts into a single sentence
            elif self.scan_type.lower() == 'full':
                source = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')), 'attack_prompts/full_scan_payloads.yaml')
                with open(source, 'r') as file:
                    data = yaml.safe_load(file)
                # Extract prompts and payloads
                return [item.get('prompt', '') for item in data.get('prompt_injections', []) if 'prompt' in item] # Join prompts into a single sentence
            elif self.scan_type.lower() == 'custom':
                source = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')), 'attack_prompts/custom_scan_payloads.yaml')
                with open(source, 'r') as file:
                    data = yaml.safe_load(file)
                # Extract prompts and payloads
                return [item.get('prompt', '') for item in data.get('prompt_injections', []) if 'prompt' in item] # Join prompts into a single sentence
       
            elif self.scan_type.lower() == 'auto':
                exit("Auto scan type is not supported yet, AI models are not yet implemented")
            else:
                exit("Please verify the scan type, valid options are: quick, full, custom and auto")
        
        
        except Exception as e:
            print(f"Error loading prompts: {e}")
            return []
        

    def run(self, target: list[str], api_key: str) -> tuple[str, bool, float]:
        provider,url,model = target  # Unpack the list into variables
    
        
        provider = provider.strip()  # Ensure no leading/trailing spaces
        model = model.strip()  # Ensure no leading/trailing spaces
        api_key = api_key.strip()  # Ensure no leading/trailing spaces
        if url.strip() == "" and provider.lower() != "openai":
            return "Url is empty", True, -1.0
        else:
            prompts = self.get_prompts()
            if prompts is None or not isinstance(prompts, list):  # {{ edit_1 }}
                LOGGER.error("Prompts list is not a valid list. Received: %s", prompts)  # Log the error
                prompts = []  # Initialize to an empty list if not valid
            total_prompts = len(prompts)
            successful_prompts = 0  # Counter for successful prompts
  # {{ edit_3 }}
    # Pl
    # ay each prompt on the specified URL
        for prompt in (prompts):
            total_tokens=0 # Initialize total tokens
            provider_functions = {  # {{ edit_7 }}
                "ollama": lambda: prompt_ollama(url, model, prompt, api_key),
                "openai": lambda: prompt_openai(url, model, prompt, api_key ),
               
              # Ensure parameters are correct
            }
            # Get the response using the provider functions or handle unsupported API types
            try:
                response = provider_functions.get(provider.lower(), lambda: "Default Unsupported API type")()  # Call the corresponding function or return default
                if provider.lower() == "openai":
                    prompt_tokens, completion_tokens, total_tokens = count_tokens(prompt, response)  
                    cost_prompt_tokens, cost_completion_tokens = calculate_cost(model, prompt_tokens, completion_tokens)
                    total_cost = cost_prompt_tokens + cost_completion_tokens
                    self.total_tokens += total_tokens
                    self.total_cost += total_cost
                 
                #LOGGER.info(f"Calling provider with parameters: provider={provider}, model={model}, prompt={prompt}, api_key={api_key}")
                attack_success, confidence_score = self.verify_attack_success(prompt,response)
                if attack_success:
                    successful_prompts += 1 # Increment the counter for successful prompts
                    self.successful_prompt_injections.append((prompt, response)) # Store the successfull promptinjection source and the confidence score when avaialble 
                    #LOGGER.info("Attack succeded", self.successful_prompt_injections)
                else:
                    #LOGGER.info("Attack failed")
                    pass
            except Exception as e:
                response = "Error during API call"
                LOGGER.error(f"API call to {provider} with parameters: url={url}, model={model}, prompt={prompt}, api_key={api_key} failed: {e}")  # Log the error
            # Further processing of the response can be done here
                
                 # Log failure

            #print(f"Response content: {response}") 
            self.results.append((prompt, response))
        success_rate = successful_prompts / total_prompts if total_prompts > 0 else 0.0

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
        scan_id = str(uuid.uuid4())  # Generate a random UUID and convert it to a string
        filename = f'attack_responses/integrity/DirectPromptInjection/{timestamp}_{scan_id}.txt'
        with open(filename, 'a') as output_file:  # Use the new filename with timestamp # {{ edit_4 }}
            for prompt, response in self.results:  # {{ edit_5 }}
                output_file.write(f"prompt: {prompt}\nresponse: {response}\n@@@@@@@@@@@@@@@\n")  # Write to the file
        
        #LOGGER.info("Attack completed with a success rate of %s", success_rate)
        return self.results, self.successful_prompt_injections, success_rate, self.total_tokens, self.total_cost # Return the conversation, successfull promptinjections with confidence score and success rate for the attack

    def verify_attack_success(self, prompt, response):
        # Call ChatGPT to validate if the response indicates a successful attack
        ai_validation_result = validation_prompt_openai(prompt, response, os.getenv("OPENAI_KEY"), "gpt-3.5-turbo").strip().lower()  # {{ edit_1 }}
        LOGGER.info(f"AI validation result from PromptInjection Plugin: {ai_validation_result}")
        if "yes" in ai_validation_result:
            score = 1  # Set the score to 1 for a successful validation
            return True, score
        else:
            score = 0  # Set the score to 0 if the validation failed
            return False, score
        
