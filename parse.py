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

def getWinner(players):
  if players[0]['is_winner']:
    return 0
  if players[1]['is_winner']:
    return 1
  return None

def getZerg(players):
  if players[0]['pick_race'] == "Zerg":
    return 0
  if players[1]['pick_race'] == "Zerg":
    return 1
  return None

def getProtoss(players):
  if players[0]['pick_race'] == "Protoss":
    return 0
  if players[1]['pick_race'] == "Protoss":
    return 1
  return None

def jsonToData(json):
  players = json['players'].values()
  winner = getWinner(players)
  zerg = getZerg(players)
  protoss = getProtoss(players)
  protossSupply = players[protoss]['supply']
  zergSupply = players[zerg]['supply']
  bothSupply = zip(protossSupply, zergSupply)
  return [(supply[0][1],supply[1][1]) for supply in bothSupply]






files = ['./data/'+f for f in os.listdir('./data/') if os.path.isfile('./data/'+f)]
print "{0} files found".format(len(files))
jsonArray = filesToJson(files)
print "{0} files loaded".format(len(jsonArray))
dataSets = map(jsonToData, jsonArray)
print "{0} json objects converted".format(len(dataSets))

flattened = [item for sublist in dataSets for item in sublist]
