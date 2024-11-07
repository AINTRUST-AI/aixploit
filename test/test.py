import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Automatically detect the current folder # Adjust this path as necessary
from dotenv import load_dotenv
load_dotenv()
from aixploit.plugins import PromptInjection 
from aixploit.core import run


target1 = ["Ollama", "http://localhost:11434/v1", "mistral"]
target2 = ["Openai", "", "gpt-3.5-turbo"]


attackers = [
    PromptInjection("quick")
    ]

#run(attackers, target1, os.getenv("OLLAMA_API_KEY"))
run(attackers, target2, os.getenv("OPENAI_KEY"))



