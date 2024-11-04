# setup.py
from setuptools import setup, find_packages

setup(
    name='aixploit',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'logging' 
    ],
    description='An AI redTeaming Python library named Aixploit',
    author='aintrust',
    author_email='contact@aintrust.ai',
    url='https://github.com/aintrustai-ai',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)