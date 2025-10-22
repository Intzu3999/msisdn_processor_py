# setup.py
from setuptools import setup, find_packages

setup(
    name="msisdn_processor_py",
    version="25.01",
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'openpyxl',
        'pandas',
        'python-dotenv',
        'requests'
    ],
)