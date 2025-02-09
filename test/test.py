import os
from datetime import datetime
from aixploit.plugins import PromptInjection, Privacy, Integrity, Availability, Abuse
from aixploit.core import run
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_KEY not found in environment variables")
if not deepseek_api_key:
    raise ValueError("DEEPSEEK_KEY not found in environment variables")


#target = ["Openai", "", "gpt-3.5-turbo"]
target2 = ["deepseek", os.getenv("DEEPSEEK_URL"), "deepseek-chat"]

attackers = [
    #PromptInjection("quick"),
    #Privacy("quick"),
    Integrity("quick"),
    #Availability("quick"),
    #Abuse("quick"),
    # PromptInjection("full")
]

start_time = datetime.now()
print("Redteaming exercise started at : ", start_time.strftime("%H:%M:%S"))

(
    conversation,
    attack_prompts,
    success_rates_percentage,
    total_tokens,
    total_cost,
) = run(attackers, target2, deepseek_api_key)

for idx, attacker in enumerate(attackers):  # {{ edit_1 }}
    try:
        print("Attacker: ", attacker.__class__.__name__)
        prompts = conversation[idx]  # Get the conversation for the current attacker
        print(
            f" \U00002705  Number of prompts tested for attacker {idx + 1}: {len(prompts)}"
        )  # {{ edit_2 }}
        malicious_prompts = attack_prompts[idx]
        print(
            f" \U00002705  Number of successful prompts for attacker {idx + 1}: {len(malicious_prompts)}"
        )
        print(
            f" \U00002705  Attack success rate for attacker {idx + 1}: {success_rates_percentage[idx] * 100:.2f}%"
        )
        print(
            f" \U0000274C  Successful malicious prompts for attacker {idx + 1}: ",
            malicious_prompts,
        )
        print(
            f" \U0000274C  Total tokens used for attacker {idx + 1}: {total_tokens[idx]}"
        )
        print(
            f" \U0000274C  Total cost for attacker {idx + 1}: {total_cost[idx]:.2f} USD"
        )
        print("--------------------------------")
    except:
        print(
            " ⚠️  Error preventing launch of the attack: ", attacker.__class__.__name__
        )

print("Redteaming exercise ended at : ", datetime.now().strftime("%H:%M:%S"))
print("Total time taken: ", datetime.now() - start_time)
