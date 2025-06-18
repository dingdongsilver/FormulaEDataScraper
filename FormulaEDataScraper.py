#from tkinter.filedialog import askopenfilename
from ast import Try
from os import name
from pydantic import BaseModel
from typing import List, Optional
import requests
import json


def getDataFromAPI(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

class Season:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.races = []

    def add_race(self, race):
        self.races.append()

class Race:
    def __init__(self, id, name, country, city, date):
        self.id = id
        self.name = name
        self.country = country
        self.city = city
        self.date = date
        sessions = []

class Session:
    def __init__(self, id, sessionName, sessionDate):
        self.id = id
        self.sessionName = sessionName
        self.sessionDate = sessionDate
        results = []

class Result:
    def __init__(self, id, driverPosition, driverId, driverCountry, driverNumber, driverTLA, driverFirstName, driverLastName, startingPosition, polePosition, fastestLap, dnf, dnq, dns, dsq, bestTime, points):
        self.id = id
        self.driverPosition = driverPosition
        self.driverId = driverId
        self.driverCountry = driverCountry
        self.driverNumber = driverNumber
        self.driverTLA = driverTLA
        self.driverFirstName = driverFirstName
        self.driverLastName = driverLastName
        self.startingPosition = startingPosition
        self.polePosition = polePosition
        self.fastestLap = fastestLap
        self.dnf = dnf
        self.dnq = dnq
        self.dns = dns
        self.dsq = dsq
        self.bestTime = bestTime
        self.points = points

   
seasonsAPIUrl = f"https://api.formula-e.pulselive.com/formula-e/v1/championships?statuses=Past,Present,Future"
raceAPIUrl = f"https://api.formula-e.pulselive.com/formula-e/v1/races?championshipId="
print(f"Fetching data from {seasonsAPIUrl}")

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

championshipResponse = requests.get(seasonsAPIUrl, headers=headers)
championshipData = championshipResponse.json()

seasons = []
races = []

for season in championshipData['championships']:
    individualSeason = Season(id=season['id'], name=season['name'])
    seasons.append(individualSeason)

for season in seasons:
    print(raceAPIUrl+season.id)
    raceResponse = requests.get(raceAPIUrl+season.id, headers=headers)
    raceData = raceResponse.json()
    for race in raceData['races']:
        individualRace = Race(id=race['id'], name=race['name'], country=race['country'], city=race['city'], date=race['date']   )
        print(f'appending {individualRace.name}')
        season.races.append(individualRace)








# for season in seasons:
#     raceResponse = requests.get(raceAPIUrl+season.id, headers=headers)
#     raceData = raceResponse.json()
#     for race in raceData['races']:
#         individualRace = Race(id=race['id'], name=race['name'], country=race['country'], city=race['city'], date=race['date'])
#         #season.races.append(individualRace)


      

# for season in data['championships']:
#     for key, value in season.items():
#         if key == 'id' and value == '88a88a4b-a48d-4d06-9e52-d609bb7824a3': #this is to limit the data while testing
#             print(value)
#             try:
#                 response = requests.get(f"{raceAPIUrl}{value}", headers=headers)
#                 response.raise_for_status()  # Raise an error for bad responses
#             except:
#                 print("Error fetching data from API. {e}")
#                 exit(1)
#             raceData = response.json()
#             for race in raceData['races']:
#                 print(race['id'])
#                 for key, value in race.items():
#                     if key == 'name':
#                         print(value)
    


