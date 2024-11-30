# aixploit

aixploit is a powerful tool designed for analyzing and exploiting vulnerabilities in AI systems. 
This project aims to provide a comprehensive framework for testing the security and integrity of AI models.
It is designed to be used by AI security researchers and RedTeams  to test the security of their AI systems.

![Alt text](https://github.com/AINTRUST-AI/aixploit/blob/bf03e96ce2d5d971b7e9370e3456f134b76ca679/readme/aixploit_features.png)

## Installation

To get started with AIxploit, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AINTRUST-AI/AIxploit.git
   cd AIxploit
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Add local variables:**
   ```bash
   touch .env
   OPENAI_KEY="sk-xxxxx"
   OLLAMA_URL="hxxp:"
   OLLAMA_API_KEY="ollama"
   ```


5. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Installation

To get started with AIxploit download the package:

```sh
pip install aixploit
```
and set the environment variables:

   export OPENAI_KEY="sk-xxxxx"
   export OLLAMA_URL="hxxp:"
   export OLLAMA_API_KEY="ollama"

## Usage

To use AIxploit, follow these steps:

1. Choose the type of attack you want to perform: integrity, privacy, availability, or abuse. 
The full list of attackers is available in the plugins folder.

2. Choose a target: OpenAI, Ollama. More targets can be added easily.

3. Update the test/test.py file with the correct target and attackers.

4. you can run the attack with the command:
   ```bash
   python test/test.py
   ```
5. The attack results will be returned automatically and the conversation will be stored in the attack_responses folder.

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
