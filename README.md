# 🐍 PYTHON PANDA 🐼

## WHAT DOES THIS PROJECT DO
1) Processes msisdn list from csv asynchronously against API to extract payload data, flattens the data structure with Panda, and output the final result in excel table.

## PYTHON BEST PRACTICE
1) We use the Pythonic way of handling API responses and extracting data. The strategy is centered around Python dictionaries!
2) Python's Naming Convention (PEP 8) are summarized below:

| Element	| Convention | Example |
|----------|----------|----------|
Script/Module names | snake_case | customer_api.py
Functions | snake_case | get_customer_data()
Variables | snake_case | customer_id
Classes | PascalCase | CustomerAPI
Constants | SCREAMING_SNAKE_CASE | MAX_RETRIES
Methods | snake_case | calculate_total()
Private variables | _snake_case	| _internal_data
Name-mangled variables | __snake_case | __private_data
Packages | lowercase | mypackage
Type variables | PascalCase	| T, ResponseType

- PEP 8 Official Guide https://peps.python.org/pep-0008/
- Python Documentation https://docs.python.org/3/tutorial/classes.html#private-variables 


## TO SETUP
1) Install python3.exe x64-bit
 verify:
 python --version
 python -c "import platform; print(platform.architecture())" 
2) At root project create new virtual env: python -m venv venv 
3) Start Python's virtual env: venv\Scripts\activate
4) python.exe -m pip install --upgrade pip
5) pip install --upgrade setuptools wheel
6) pip install -r requirements.txt
 if panda failing it is most likely due to your venv setup.
 pip install --upgrade setuptools wheel meson ninja cython numpy (and any other missing/failed dependency installation based from your log)
 pip install --force-reinstall --no-cache-dir pandas
7) To close Python's virtual env: deactivate

## TO RUN TEST
1) python tests/api_regression.test.py

## TO RUN DATA PROCESSING SCRIPT
1) python run_api.py (defaults to test dataStream and get_subscriber_api service)
2) python run_all_api.py celcom --service get_customer_api

## WORK IN PROGRESS ... 
1) get_account_structure_api 
2) chain API calls
3) Standardize API calls design according to Python's best practice

## TO LEARN AND IMPROVE
1) Strategy Pattern using Python's Registry and abc abstract method classes
2) async with async_timeout.timeout(10):  # 10 second timeout
3) Configure service_rate_limiter at config level
4) import logging . Replace prints with logger.info()
5) Save processed data to local MySQL. Require: design appropriate db design.