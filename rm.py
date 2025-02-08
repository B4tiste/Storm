import os
import sys
import json

folder_path = '/home/batiste/Documents/Storm/tl_raw_data'

for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data.get('season') is None and data.get('version') is None:
                os.remove(file_path)
                print(f"Deleted {file_path}")