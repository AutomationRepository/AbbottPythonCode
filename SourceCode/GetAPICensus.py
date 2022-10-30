import collections
import json
import sys
from datetime import datetime

import requests

start_time = datetime.now().microsecond

URL = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"

# load the response based on the URL specified
try:
    request = requests.get(url=URL)
    response = request.json()
    # f = open('C:\\Users\\Neha\\PycharmProjects\\AbbottCodeChallenge\\data1.json')
    # response = json.load(f)
except:
    sys.tracebacklimit = 0
    print("Please validate the URL and make sure that the server is up")
    sys.exit(1)

# Validate that the information needed is present in the response
if 'data' not in response:
    sys.tracebacklimit = 0
    print("The API response seems to be corrupted as the data is missing")
    sys.exit(1)
elif 'source' not in response:
    sys.tracebacklimit = 0
    print("The API response seems to be corrupted as the source information is missing----1")
    sys.exit(1)

for source in response['source']:
    try:
        if source['annotations']:
            source_name = source['annotations']['source_name']
    except:
        # sys.tracebacklimit = 0
        print("The API response seems to be corrupted as the annotations or the source name is missing")
        sys.exit(1)

# Empty dict for storing key-Value pair
infoDict = {}

# collecting the data into Dictionary and exiting the program if there are any duplicate years(Keys) in response
for data in response['data']:
    if data['ID Year'] in infoDict.keys():
        sys.tracebacklimit = 0
        print("The API response seems corrupted as there are more than 1 data set for Year", data['ID Year'])
        sys.exit(1)
    infoDict[data['ID Year']] = data['Population']

# sorting the data on the basis of year to identify the start and end
sortedByYear = list(sorted(infoDict.items(), key=lambda x: x[0]))
startDate = sortedByYear[0][0]
endDate = sortedByYear[len(sortedByYear) - 1][0]

# identifying the population for the first year in order to compare the years ahead.
basePopulation = sortedByYear[0][1]
baseYear = sortedByYear[0][0]
if len(sortedByYear) == 1:  # if only single value is present, halt the program with message
    sys.tracebacklimit = 0
    print("The Population data is not sufficient to calculate the population peak/lowest increase")
    sys.exit(1)
elif len(sortedByYear) == 2:
    if sortedByYear[1][1] < basePopulation:
        sys.tracebacklimit = 0
        print("The Population data is not sufficient to calculate the population peak/lowest increase")
        sys.exit(1)
    else:
        highestPopulationYear = sortedByYear[1][0]
        highestPopulation = sortedByYear[1][1]
        lowestPopulation = sortedByYear[0][1]
        lowestPopulationYear = sortedByYear[0][0]
        lowestIncrease = peakIncrease = ((highestPopulation - lowestPopulation) / lowestPopulation) * 100
else:
    flagInitial = 0
    highestPopulation = 0
    lowestPopulation = 0
    secondLowestPopulation = 0
    # print(infoDict)
    for data in response['data']:
        infoDict[data['ID Year']] = data['Population']
        # list.append(infoDict)
        if data['Population'] < basePopulation:
            print("less than base", data['ID Year'])
        else:

            if flagInitial == 0:
                highestPopulation = lowestPopulation = basePopulation
                lastUpdateKey = lowestPopulationYear = highestPopulationYear = baseYear
                lastUpdatePopulation = secondLowestPopulation = data['Population']
                lastUpdateYear = data['ID Year']
                flagInitial = 1
            if flagInitial == 1 and highestPopulation < data['Population']:
                highestPopulation = data['Population']
                highestPopulationYear = data['ID Year']
            if flagInitial == 1 and secondLowestPopulation > data['Population'] > lowestPopulation:
                secondLowestPopulation = data['Population']
                lowestPopulationYear = data['ID Year']
            lastUpdatePopulation = data['Population']
            lastUpdateYear = data['ID Year']
            peakIncrease = ((highestPopulation - lowestPopulation) / lowestPopulation) * 100
            lowestIncrease = ((secondLowestPopulation - lowestPopulation) / lowestPopulation) * 100

    # print(peakIncrease)
    # print(lowestIncrease)
    # print(highestPopulation)
    # print(lowestPopulation)
    # print(secondLowestPopulation)

    result = 'According to ' + str(source_name) + ', in ' + str(len(response['data'])) + ' years from ' + str(
        startDate) + ' to ' + str(endDate) + \
             ', peak population growth was ' + str(round(peakIncrease, 2)) + '% in \n' + str(highestPopulationYear) + \
             ' and lowest population increase was ' + str(round(lowestIncrease, 2)) + '% in ' + str(
        lowestPopulationYear) + '.'

    print(result)

    end_time = datetime.now().microsecond
    # print('Duration in Micro-seconds: {}'.format(end_time - start_time))
