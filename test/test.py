import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Automatically detect the current folder # Adjust this path as necessary
from dotenv import load_dotenv
load_dotenv()
from aixploit.plugins import PromptInjection
from aixploit.core import run


target1 = ["Ollama", "http://localhost:11434/v1", "mistral"]
target2 = ["Openai", "", "gpt-3.5-turbo"]


attackers = [
    PromptInjection("quick"),
    #PromptInjection("full")
    ]

#conversation, attack_prompts_malicious, success_rates_percentage = run(attackers, target1, os.getenv("OLLAMA_API_KEY"))
conversation, attack_prompts_malicious, success_rates_percentage = run(attackers, target2, os.getenv("OPENAI_KEY"))

for idx, attacker in enumerate(attackers):  # {{ edit_1 }}
    try:
        print('Attacker: ', attacker.__class__.__name__)  
        prompts = conversation[idx]  # Get the conversation for the current attacker
        #print(f'\U0001F4AC Conversation for attacker {idx + 1}: \n {prompts} \n End of conversation')  # {{ edit_1 }}
        malicious_prompts = attack_prompts_malicious[idx]
        print(f' \U00002705  Attack success rate for attacker {idx + 1}: ', success_rates_percentage[idx])
        print(f' \U0000274C  Successful malicious prompts for attacker {idx + 1}: ', malicious_prompts)
        print('--------------------------------')
    except:
        print(' ⚠️  No conversation found for attacker: ', attacker.__class__.__name__)
