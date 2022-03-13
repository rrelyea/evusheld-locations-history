from fileinput import filename
import os
import sys
from os.path import exists
from pandas import to_numeric
from urllib.parse import urlparse

def getCounty(fullCountyName):
  county = before(fullCountyName, ",")[1:]
  if "County" in county:
    county = before(county, " County")
  return county

def getState(fullCountyName):
  state = after(fullCountyName, ", ")
  state = state[0:len(state)-1]
  return state

def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]

def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1: return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]

def createCountyAdjacenyFiles(localBasePath):
  with open(localBasePath + "data/county-adjacency/county_adjacency.txt", "r") as countiesFile:
    currentCounty = ""
    currentState = ""
    currentCountyNumber = 0
    file = None
    lineNo = 0
    while True:
      line = countiesFile.readline()

      # if line is empty
      # end of file is reached
      if not line:
          break
  
      chunks = line.split('\t')
      if chunks[0] != '':
        currentCounty = getCounty(chunks[0])
        currentState = getState(chunks[0])
        currentCountyNumber = to_numeric(chunks[1][0:5])
        if currentState == '':
          sys.exit("errored at line: " + str(lineNo))
        targetPath = localBasePath + "data/county-adjacency/" + currentState + "/" 
        countyFile = targetPath + currentCounty.lower() + ".csv" 

        while not os.path.exists(targetPath):
          os.mkdir(targetPath)
        if file != None:
          file.close()
        file = open(countyFile, 'w')
      adjacentCounty = getCounty(chunks[2])
      adjacentState = getState(chunks[2])
      adjacentCountyNumber = to_numeric(chunks[3][0:5])
      file.write(adjacentCounty.lower() + "," + adjacentState + '\n')
      lineNo = lineNo + 1
    file.close()

if len(sys.argv) > 1 and sys.argv[1] == 'onServer':
  localBasePath = ""
else:
  localBasePath = "../../"

createCountyAdjacenyFiles(localBasePath)
