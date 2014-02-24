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
  return [(supply[0][1],supply[1][1], 1 if winner == zerg else 0) for supply in bothSupply]

def median(data):
  if data == []:
    return None
  return sorted(data)[int(len(data)/2)]

def getRange(data, starti, endi):
  filtered = filter(lambda x: x[0] >= starti and x[0] < endi, data)
  filteredZ = map(lambda x: x[1], filter(lambda x: x[2] == 0, filtered))
  filteredP = map(lambda x: x[1], filter(lambda x: x[2] == 1, filtered))
  return "{0}, {1}".format(median(filteredZ), median(filteredP))




files = ['./data/'+f for f in os.listdir('./data/') if os.path.isfile('./data/'+f)]
print "{0} files found".format(len(files))
jsonArray = filesToJson(files)
print "{0} files loaded".format(len(jsonArray))
dataSets = map(jsonToData, jsonArray)
print "{0} json objects converted".format(len(dataSets))

flattened = [item for sublist in dataSets for item in sublist]
flatString = map((lambda x: "{0},{1},{2}".format(x[0], x[1], x[2])),flattened)
f = file("out.csv", "w")
f.write("\n".join(flatString))
f.close()

supplySpread = 5
supplyMin = 10
supplyMax = 180
supplyRanges = map(lambda x: (x * supplySpread, (x + 1) * supplySpread), range(supplyMin/supplySpread, supplyMax / supplySpread-1))

computed = map(lambda x: "{0}, {1}".format(x[0], getRange(flattened, x[0], x[1])), supplyRanges)

f = file("pvz.csv", "w")
f.write("\n".join(computed))
f.close()
