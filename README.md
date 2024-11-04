# AIxploit

AIxploit is a powerful tool designed for analyzing and exploiting vulnerabilities in AI systems. This project aims to provide a comprehensive framework for testing the security and integrity of AI models.


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

   ```


5. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use AIxploit, follow these steps:

1. Check the plugins folder to see the available attacks.

2. Choose an attack and modify the payloads in the payloads folder.

3. Run the attack with the command:
   ```bash
   python test/test.py
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