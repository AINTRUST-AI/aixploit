# AIxploit



[![Downloads](https://static.pepy.tech/badge/aixploit)](https://pepy.tech/project/aixploit)
[![PyPI - Python Version](https://img.shields.io/pypi/v/aixploit)](https://pypi.org/project/aixploit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://static.pepy.tech/badge/aixploit/month)](https://pepy.tech/project/aixploit)


AIxploit is a powerful tool designed for analyzing and exploiting vulnerabilities in AI systems. 
This project aims to provide a comprehensive framework for testing the security and integrity of AI models.
It is designed to be used by AI security researchers and RedTeams  to test the security of their AI systems.

See more in the [**Documentation**](https://docs.aintrust.ai/aixploit)

![Alt text](https://github.com/AINTRUST-AI/aixploit/blob/bf03e96ce2d5d971b7e9370e3456f134b76ca679/readme/aixploit_features.png)

## Installation

To get started with AIxploit download the package:

```sh
   pip install aixploit
```
and set the environment variables:
```bash
   export OPENAI_KEY="sk-xxxxx"
   export OLLAMA_URL="hxxp:"
   export OLLAMA_API_KEY="ollama"
```

## Usage

To use AIxploit, follow these steps:

1. Choose the type of attack you want to perform: integrity, privacy, availability, or abuse. 
The full list of attackers is available in the plugins folder.
   ```bash
   from aixploit.plugins import PromptInjection
   ```
2. Choose your targets and the associated attackers.
   ```bash
   target = ["Ollama", "http://localhost:11434/v1", "mistral"]
   attackers = [
        Privacy("quick"),
        Integrity("full"),
        Availability("quick"),
        Abuse("custom"),
   ] 
   ```

3. Run your attack and analyze the results:
   ```bash
   run(attackers, target, os.getenv("OLLAMA_API_KEY"))
   ```


Example test.py:

```bash

    import os
    from datetime import datetime
    from aixploit.plugins import PromptInjection, Privacy, Integrity, Availability, Abuse
    from aixploit.core import run


    target = ["Openai", "", "gpt-3.5-turbo"]
    attackers = [   
        PromptInjection("quick"),
        Privacy("quick"),
        Integrity("quick"),
        Availability("quick"),
        Abuse("quick"),
        #PromptInjection("full")
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

```

## Contributing

We welcome contributions to AIxploit! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.


## Contact

For any inquiries or feedback, please contact:

- **Contact AINTRUST AI** - [contact@aintrust.ai](mailto:contact@aintrust.ai)
- **Project Link**: [AIxploit GitHub Repository](https://github.com/AINTRUST-AI/AIxploit)

---

Thank you for your interest in AIxploit! We hope you find it useful.
