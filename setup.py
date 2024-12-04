from setuptools import setup, find_packages


packages = find_packages()

setup(
    name="aixploit",
    packages=packages,
    description="AI redTeaming Python library",
    author="aintrust",
    author_email="contact@aintrust.ai",
    url="https://github.com/AINTRUST-AI/AIxploit",
    keywords=[
        "AI",
        "redteaming",
        "AI redteaming",
        "AI redteam",
        "AI redteaming library",
        "AI redteam library",
        "LLM",
        "LLMs",
        "LLM Guardrails",
        "LLM Security",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
