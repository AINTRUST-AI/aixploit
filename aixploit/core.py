import time
import logging 
from typing import List  # Import the logging module
from .plugins.base import Attacker as RedTeamAttacker


"""
This module implements the core functionality for executing Red Teaming tasks on Large Language Models (LLMs).
The primary function, 'run', orchestrates the application of a list of attacker objects against a specified URL or API endpoint.

In this context, an Attacker is an instance of a class that inherits from the base class 'Attacker'.
Each subclass must implement the `run` method, which accepts parameters including a string input and returns a tuple containing:
- A processed string resulting from the attack.
- A boolean indicating the validity of the input string after processing.
- Additional metrics or scores as required.

The 'run' function aggregates the results from all attacker instances, returning:
- The final processed string after all attacks have been applied.
- A dictionary mapping each attacker's name to its validity result.
- A dictionary containing risk scores or other relevant metrics associated with each attacker.

This design allows for extensibility, enabling the addition of new attacker types with varying strategies for manipulating input data and assessing the security posture of LLMs.
"""
logging.basicConfig(level=logging.INFO)  # Set the logging level
LOGGER = logging.getLogger(__name__)  # Create a logger for this module


def run(
    attackers: List[RedTeamAttacker],  # Change list to List
    provider: str,
    url: str,
    model: str,
    api_key: str,
    fail_fast: bool = False
) -> tuple[str, dict[str, bool], dict[str, float]]:
 
    """
    Try to run an attack on a given url using the provided attackers.

    Args:
        attackers: A list of attacker objects. Each attacker should be an instance of a class that inherits from `Attacker`.
        url: The target URL that needs to be tested.
        provider: The provider of the LLM model.
        model: The model targeted with the attack.
        api_key: The API key to be used for the attack.
        fail_fast: A boolean value indicating whether to stop scanning after the first scanner fails.

    Returns:
        A tuple containing:
            - The processed prompt string after applying all attackers.
            - A dictionary mapping attackers names to boolean values indicating whether the input prompt is valid according to each scanner.
            - A dictionary mapping scanner names to float values of risk scores, where 0 is no risk, and 1 is high risk.
    """
   
    results_score = {}
    # Initialize an empty list to store all attack prompts # Initialize an empty list to store all attack prompts
    

    
    if len(attackers) == 0 :
        return results_score

    start_time = time.time()
    attack_prompts = [] #  the list of prompts for all the attackers need to be returned 
    attack_prompts_list = [] # the list of prompts cleared after each attacker 
    for attacker in attackers:
        success_rates = []
        start_time_attacker = time.time()
        elapsed_time_attacker = 0  # Initialize the variable
        
        if hasattr(attacker, 'run'):
            attack_prompt,is_valid, success_rate = attacker.run(provider,url,model,api_key)
            attack_prompts.append(attack_prompt)
            attack_prompts_list.append(attack_prompt)
            success_rates.append(success_rate)

            # Calculate elapsed time for the current attacker
            elapsed_time_attacker = time.time() - start_time_attacker
        else:
            LOGGER.error(f"{type(attacker).__name__} does not have the method 'run'")
            continue 
        
         # Using str() to convert the dictionary to a string
       

        if success_rates and len(attack_prompts[0])>0:  # Check if the list is not empty
            average_success_rate = sum(success_rates) / len(attackers)  # Calculate average
            success_rates_percentage = f"{average_success_rate * 100:.2f}%"  # Format as percentage
        else:
            success_rates_percentage = "0.00%"  # ntage

        attacker_name = type(attacker).__name__  # Get the name of the attacker class
        #LOGGER.info("Attack completed %s succeeded by %s: on provider: %s in %.6f seconds, with a success rate of %s ", len(success_rates),attacker_name, provider , round(elapsed_time_attacker, 6), success_rates_percentage)
        
        if fail_fast and not is_valid:
            break
    
    # Convert success rates to percentage format    
    elapsed_time = time.time() - start_time
    #LOGGER.info("Malicious prompt: prompts=%s, elapsed_time_seconds=%.6f", attack_prompts, round(elapsed_time, 6))  # {{ edit_1 }}
    #LOGGER.info("Number of prompts: %s", len(attack_prompts[0]))  # {{ edit_1 }}
    LOGGER.info("RedTeaming Task completed: %s attackers, prompts=%s, elapsed_time_seconds=%.6f, with a success rate of %s", len(attackers) , len(attack_prompts_list[0])    , round(elapsed_time, 6), success_rates_percentage)  # {{ edit_1 }}
    attack_prompts_list[0].clear()    # Clear the list of prompts after each attacker
    return attack_prompts, is_valid, success_rates_percentage
