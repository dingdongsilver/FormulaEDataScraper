# Import necessary libraries (unnecessary ones too)
#=======================================================
from ast import Try
from dataclasses import asdict, dataclass
from os import name
from pydantic import BaseModel
from typing import List, Optional
import requests
import json
import logging
#-------------------------------------------------------
# Set up logging
#=======================================================
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('FormulaEDataScraper.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('Starting Formula E Data Scraper')
#-------------------------------------------------------
# Define functions and data models
# =======================================================
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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "races": [r.to_dict() for r in self.races]
        }

class Race:
    def __init__(self, id, name, country, city, date):
        self.id = id
        self.name = name
        self.country = country
        self.city = city
        self.date = date
        self.sessions = []
        self.results = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country, 
            "city": self.city,
            "date": self.date,
            "sessions": [s.to_dict() for s in self.sessions],
            "results": [r.to_dict() for r in self.results]
            }

class Session:
    def __init__(self, id, sessionName, sessionDate):
        self.id = id
        self.sessionName = sessionName
        self.sessionDate = sessionDate
        results = []

        def to_dict(self):
            return {
                "id": self.id,
                "sessionName": self.sessionName, 
                "sessionDate": self.sessionDate,
                "results": [r.to_dict() for r in self.results]
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "driverPosition": self.driverPosition,
            "driverId": self.driverId,
            "driverCountry": self.driverCountry,
            "driverNumber": self.driverNumber,
            "driverTLA": self.driverTLA,
            "driverFirstName": self.driverFirstName,
            "driverLastName": self.driverLastName,
            "startingPosition": self.startingPosition,
            "polePosition": self.polePosition,
            "fastestLap": self.fastestLap,
            "dnf": self.dnf,
            "dnq": self.dnq,
            "dns": self.dns,
            "dsq": self.dsq,
            "bestTime": self.bestTime,
            "points": self.points
        }
# -------------------------------------------------------
# Define API URLs
# =======================================================
seasonsAPIUrl = f"https://api.formula-e.pulselive.com/formula-e/v1/championships?statuses=Past,Present,Future"
raceAPIUrl = f"https://api.formula-e.pulselive.com/formula-e/v1/races?championshipId="
sessionAPIUrl = "https://api.formula-e.pulselive.com/formula-e/v1/races/{}/sessions?groupQualifyings=true&onlyActualEvents=true"
resultsAPIUrl = "https://api.formula-e.pulselive.com/formula-e/v1/races/{}/sessions/{}/results"
# -------------------------------------------------------
# Set up headers for the requests
# =======================================================
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# -------------------------------------------------------
# Fetch championship data from the API, this is the seasons/years
# =======================================================
championshipResponse = requests.get(seasonsAPIUrl, headers=headers)
championshipData = championshipResponse.json()
# -------------------------------------------------------
# Arrays to hold objects
# =======================================================
seasons = []
races = []
# -------------------------------------------------------
# Load all of the seasons into objects
# =======================================================
logger.info(f"Fetching data from {seasonsAPIUrl}")
for season in championshipData['championships']:
    individualSeason = Season(id=season['id'], name=season['name'])
    # Comment the if statement to see all seasons
    if individualSeason.id == "88a88a4b-a48d-4d06-9e52-d609bb7824a3":
        seasons.append(individualSeason)
# -------------------------------------------------------
# Iterate through seasons to get race information
# =======================================================
for season in seasons:
    logging.debug(f"Fetching season from {raceAPIUrl}{season.id}")
    raceResponse = requests.get(raceAPIUrl+season.id, headers=headers)
    raceData = raceResponse.json()
    # --------------------------------------------------------
    # Load all the races into objects
    # ========================================================
    for race in raceData['races']: 
        individualRace = Race(id=race['id'], name=race['name'], country=race['country'], city=race['city'], date=race['date']   )
        logger.info(f'Appending {individualRace.name}')
        season.races.append(individualRace)
        logger.debug(f"Fetching sessions from {sessionAPIUrl.format(individualRace.id)}")
        # --------------------------------------------------------
        # Get all sessions for all races (we're only going to load the race session, not FP1, FP2, etc.)
        # ========================================================
        session = requests.get(sessionAPIUrl.format(individualRace.id))
        session = session.json() 
        for item in session['sessions']:
            if item['sessionName'] == "Race":
                sessionID = item['id']
        # --------------------------------------------------------
        # Get and load all of the race results into objects
        # ========================================================
        raceResults = requests.get(resultsAPIUrl.format(individualRace.id, sessionID), headers=headers)
        raceResults = raceResults.json()  
        for result in raceResults:
            individualResult = Result(id=result['id'], driverPosition=result['driverPosition'], driverId=result['driverId'], driverCountry=result['driverCountry'], driverNumber=result['driverNumber'], driverTLA=result['driverTLA'], driverFirstName=result['driverFirstName'],
                                      driverLastName=result['driverLastName'], startingPosition=result['startingPosition'], polePosition=result['polePosition'], fastestLap=result['fastestLap'], dnf=result['dnf'], dnq=result['dnq'], dns=result['dns'], dsq=result['dsq'], bestTime=result['bestTime'], points=result['points'])
            logging.info(f'Appending {individualResult.driverFirstName} {individualResult.driverLastName}')
            individualRace.results.append(individualResult)

season_dicts = [s.to_dict() for s in seasons]

with open('formulae_data.json', 'w') as f:
    f.write(json.dumps(season_dicts, indent=4))
