# 🐍 PYTHON PANDA 🐼

# WHAT DOES THIS PROJECT DO
1) Processes hundreds of msisdn asynchronously against multiple APIs to get relevant payload details, flattens the data structure with Panda, and output the final result in excel table.


# PYTHON BEST PRACTICE
1) snake_case is preferred in Python (it is a ssssnake!)
2) We follow the Pythonic way of handling API responses and extracting data. The strategy is centered around Python dictionaries!
3) Safe data extraction using .get()! List safely to prevent IndexError when accessing nested lists. No crashes if payload is missing.

# TO SETUP
1) have python3 installed
2) pip install -r requirements.txt

# TO RUN TEST
1) python test/test_script_name.test.py

# TO RUN DATA PROCESSING SCRIPT
1) python read_csv.py
2) python read_csv.py csvFileName --service servine_name

# TO ADD / BUILD 
1) get_subscriber-api, get_account_structure_api 
3) chain API calls

# TO LEARN AND IMPROVE
1) logging and sys
2) typing schema