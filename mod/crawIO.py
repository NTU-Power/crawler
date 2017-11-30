from tabulate import tabulate
def printPowerData(powerDataTuple):
    (powerAttrs, powerData) = powerDataTuple
    print(powerAttrs)
    print(tabulate(powerData))
    print('')

def printMeters(meterTuples):
    print(tabulate(meterTuples))

def dumpMetersCSV(meterTuples, csvFileName):
    with open(csvFileName, 'w') as csvFile:
        csvFile.write('MeterID,MeterName\n')
        for oneTuple in meterTuples:
            csvFile.write(oneTuple[0]+','+oneTuple[1]+'\n')

def loadMetersCSV(csvFileName):
    with open(csvFileName) as csvFile:
        csvLines = csvFile.readlines()
        meterIDs = [a.split(',')[0] for a in csvLines[1:]]
        meterNames = [a.split(',')[1][0:-1] for a in csvLines[1:]]
    return meterIDs, meterNames
