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
        results = []

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
sessionAPIUrl = "https://api.formula-e.pulselive.com/formula-e/v1/races/{}/sessions?groupQualifyings=true&onlyActualEvents=true"
resultsAPIUrl = "https://api.formula-e.pulselive.com/formula-e/v1/races/{}/sessions/{}/results"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

championshipResponse = requests.get(seasonsAPIUrl, headers=headers)
championshipData = championshipResponse.json()

seasons = []
races = []

print(f"Fetching data from {seasonsAPIUrl}")
for season in championshipData['championships']:
    individualSeason = Season(id=season['id'], name=season['name'])
    seasons.append(individualSeason)

for season in seasons:
    #print(raceAPIUrl+season.id)
    raceResponse = requests.get(raceAPIUrl+season.id, headers=headers)
    raceData = raceResponse.json()
    for race in raceData['races']: #load up all the races into objects
        individualRace = Race(id=race['id'], name=race['name'], country=race['country'], city=race['city'], date=race['date']   )
        #print(f'appending {individualRace.name}')
        season.races.append(individualRace)
        #now get the session ID for the race
        #print (sessionAPIUrl.format(individualRace.id))
        session = requests.get(sessionAPIUrl.format(individualRace.id))
        session = session.json()  # convert to json
        for item in session['sessions']:
            #print(item['sessionName'])
            if item['sessionName'] == "Race":
                sessionID = item['id']
        raceResults = requests.get(resultsAPIUrl.format(individualRace.id, sessionID), headers=headers)
        raceResults = raceResults.json()  # convert to json
        for result in raceResults:
            individualResult = Result(id=result['id'], driverPosition=result['driverPosition'], driverId=result['driverId'], driverCountry=result['driverCountry'], driverNumber=result['driverNumber'], driverTLA=result['driverTLA'], driverFirstName=result['driverFirstName'],
                                      driverLastName=result['driverLastName'], startingPosition=result['startingPosition'], polePosition=result['polePosition'], fastestLap=result['fastestLap'], dnf=result['dnf'], dnq=result['dnq'], dns=result['dns'], dsq=result['dsq'], bestTime=result['bestTime'], points=result['points'])
            # print(f'appending {individualResult.driverFirstName} {individualResult.driverLastName}')
            individualRace.results.append(individualResult)