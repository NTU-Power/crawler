from tabulate import tabulate
def printPowerData(powerDataTuple):
    (powerAttrs, powerData) = powerDataTuple
    print(powerAttrs)
    print(tabulate(powerData))
    print('')

def printBuildings(buildingTuples):
    print(tabulate(buildingTuples))

def dumpBuildingsCSV(buildingTuples, csvFileName):
    with open(csvFileName, 'w') as csvFile:
        csvFile.write('BuildingID,BuildingName\n')
        for oneTuple in buildingTuples:
            csvFile.write(oneTuple[0]+','+oneTuple[1]+'\n')
