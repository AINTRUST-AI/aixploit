from setuptools import setup, find_packages


packages = find_packages(include=['aixploit*'], exclude=['tests*'])

# Print the discovered packages
print("Discovered packages:", packages)
setup(
    name='aixploit',
    packages=packages,
    description='An AI redTeaming Python library named Aixploit',
    author='aintrust',
    author_email='contact@aintrust.ai',
    url='https://github.com/aintrustai-ai/aixploit',  # Update with your repository URL
    keywords = ["AI", "redteaming", "AI redteaming", "AI redteam", "AI redteaming library", "AI redteam library", "LLM", "LLMs"],  # Added missing closing bracket

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # Updated classifier
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
