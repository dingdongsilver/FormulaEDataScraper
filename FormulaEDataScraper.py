#from tkinter.filedialog import askopenfilename
import requests
import json

seasonsAPIUrl = f"https://api.formula-e.pulselive.com/formula-e/v1/championships?statuses=Past,Present,Future"
print(f"Fetching data from {seasonsAPIUrl}")

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(seasonsAPIUrl, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
except:
    print("Error fetching data from the API. {e}")
    exit(1)

data = response.json()

for race in data['championships']:
    for key, value in race.items():
        if key == 'id':
            print(f"Getting races for {value}")


