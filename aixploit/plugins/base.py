import abc
from typing import Protocol

class Attacker(Protocol):
    """
    Attacker protocol that defines the interface for attackers.
 """

    @abc.abstractmethod
    def run(self, provider: str, url: str, model: str, api_key: str) -> tuple[str, bool, float]:
        """
        Run an attack according to the specific plugin's implementation.

        Parameters:
            provider (str): The provider targeted with the attack. Ollama, OpenAI, etc.
            url (str): The target URL that needs to be tested.
            model (str): The model targeted with the attack. gpt-3.5-turbo, claude-3-5-sonnet, etc.
            api_key (str): The API key to be used for the attack.  

        Returns:
            str: The processed prompt as per the attacker's implementation.
            bool: A flag indicating whether the prompt is valid or not.
            float: Risk score where 0 means no risk and 1 means high risk.
        """