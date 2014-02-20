import json
import os

def readFile(name):
  return open(name, 'r').read()

def readFileToJsonObj(name):
  return json.loads(readFile(name))

def is1v1(json):
  return json['game_type'] == "1v1"

def isLadder(json):
  return json['category'] == "Ladder"

def getMatchup(json):
  if len(json['players']) == 2:
    return sorted([json['players'].values()[0]['pick_race'],json['players'].values()[1]['pick_race']])
  return None


def isPvZ(json):
  return getMatchup(json) == ["Protoss", "Zerg"]

def isFilteredGame(json):
  return isPvZ(json)

def filesToJson(names):
  return [readFileToJsonObj(name) for name in names if isFilteredGame(readFileToJsonObj(name))]




files = [f for f in os.listdir('.') if os.path.isfile(f)]
jsonArray = filesToJson(files)
print len(jsonArray)
