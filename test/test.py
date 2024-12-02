import os
from datetime import datetime
from aixploit.plugins import PromptInjection, Privacy
from aixploit.core import run


target = ["Openai", "", "gpt-3.5-turbo"]
attackers = [
    PromptInjection("quick"),
    #Privacy("quick"),
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
) = run(attackers, target, os.getenv("OPENAI_KEY"))

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
