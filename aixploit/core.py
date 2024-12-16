import time
import logging  # Import the logging module
from typing import List
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
- A dictionary mapping each attacker to its conversation (prompts + responses).
- A dictionary mapping each attacker to its successful malicious conversations (prompts + responses).
- A dictionary mapping each attacker to its successful rates or o 
- A dictionary containing attack success rates / risk scores or other relevant metrics associated with each attacker.

This design allows for extensibility, enabling the addition of new attacker types with varying strategies 
for manipulating input data and assessing the security posture of LLMs.
"""

logging.basicConfig(level=logging.INFO)  # Set the logging level for your module
httpx_logger = logging.getLogger("httpx")  # Get the httpx logger
httpx_logger.setLevel(
    logging.WARNING
)  # Set the logging level to WARNING to hide it in INFO logs
LOGGER = logging.getLogger(__name__)  # Create a logger for this module


def run(
    attackers: List[RedTeamAttacker],  # Change list to List
    target: list[str],
    api_key: str,
) -> tuple[str, dict[str, bool], dict[str, float]]:
    """
    Try to run an attack on a given url using the provided attackers.

    Args:
        attackers: A list of attacker objects. Each attacker should be an instance of a class that inherits from `Attacker`.
        target: A list containing the provider, url, and model.
        - provider (str): The provider targeted with the attack. Ollama, OpenAI, etc.
        - url (str): The target URL that needs to be tested.
        - model (str): The model targeted with the attack. gpt-3.5-turbo, claude-3-5-sonnet, etc.
        api_key: The API key to be used for the attack.

    Returns:
        A tuple containing:
            - The processed prompt string after applying all attackers.
            - A dictionary mapping attackers names to boolean values indicating whether the input prompt is valid according to each scanner.
            - A dictionary mapping scanner names to float values of risk scores, where 0 is no risk, and 1 is high risk.
    """

    # Initialize an empty list to store all attack prompts
    if len(attackers) == 0:
        LOGGER.error(" No attackers provided")
        return "No attackers provided"

    start_time = time.time()  # Start timer for the entire RedTeaming task
    attack_prompts_full = []  # Initialize an empty list to store all conversations
    successful_attack_prompts_full = (
        []
    )  # Initialize an empty list to store successful malicious prompts
    success_rates_full = (
        []
    )  # Initialize an empty list to store success rates for each attacker
    total_tokens_full = (
        []
    )  # Initialize an empty list to store total tokens for each attacker
    total_cost_full = (
        []
    )  # Initialize an empty list to store total cost for each attacker
    for (
        attacker
    ) in attackers:  # Initialize an empty list to store success rates for each attacker
        start_time_attacker = time.time()  # Start timer for the current attacker

        if hasattr(attacker, "run"):  # Check if the attacker has the 'run' method
            (
                attack_prompts,
                malicious_prompts,
                success_rate,
                total_tokens,
                total_cost,
            ) = attacker.run(
                target, api_key
            )  # Run the attacker and return the conversation, successful malicious prompts and the success rate
            attack_prompts_full.append(
                attack_prompts
            )  # Store the conversation of all attackers
            successful_attack_prompts_full.append(
                malicious_prompts
            )  # Store the successful malicious prompts of all attackers
            success_rates_full.append(
                success_rate
            )  # Store the success rate of all attackers
            total_tokens_full.append(
                total_tokens
            )  # Store the total tokens of all attackers
            total_cost_full.append(total_cost)  # Store the total cost of all attackers
            # Calculate elapsed time for the current attacker
            elapsed_time_attacker = time.time() - start_time_attacker
        else:
            LOGGER.error(
                f"{type(attacker).__name__} does not have the method 'run'"
            )  # Log an error if the attacker does not have the 'run' method
            continue
        # Using str() to convert the dictionary to a string

        # attacker_name = type(attacker).__name__  # Get the name of the attacker class
        # elapsed_time_attacker = time.time() - start_time_attacker
        # LOGGER.info("Conversation =%s, took place via %s  in an elapsed_time_seconds=%.6f", attack_prompts if attack_prompts else "No prompts", attacker_name, round(elapsed_time_attacker, 6))

    # elapsed_time = time.time() - start_time
    # total_prompts_number = sum(len(sublist) for sublist in attack_prompts_full)
    # LOGGER.info(" Total number of prompts: %s", total_prompts_number)
    # LOGGER.info(" RedTeaming Task completed: %s attackers, prompts=%s, elapsed_time_seconds=%.6f, with a success rate of %s", len(attackers) , total_prompts_number    , round(elapsed_time, 6), success_rates_percentage)  # {{ edit_1 }}   # Clear the list of prompts after each attacker
    return (
        attack_prompts_full,
        successful_attack_prompts_full,
        success_rates_full,
        total_tokens_full,
        total_cost_full,
    )
