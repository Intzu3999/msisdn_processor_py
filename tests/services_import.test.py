#checks paths, exports, and imports in the /services folder are defined and traceable.
#copy command, paste into terminal in project root

python read_csv.py test --service customer
python read_csv.py test --service checkBlacklist # API function not developed yet
python read_csv.py test --service subscriber # API function not developed yet
python read_csv.py test --service accountStructure # API function not developed yet
python read_csv.py test --service account # not yet mapped n api_map
python read_csv.py test --service familyGroup # not yet mapped in api_map