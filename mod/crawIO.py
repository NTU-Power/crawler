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

def loadMappingCSV(csvFileName):
    with open(csvFileName) as csvFile:
        csvLines = csvFile.readlines()
        buildingIDs     = [a.split(',')[0] for a in csvLines[1:]]
        buildingNames   = [a.split(',')[1] for a in csvLines[1:]]
        PowerMeterStrs  = [a.split('"')[1] for a in csvLines[1:]]

        PowerMeterCleanStrs = [0]*len(PowerMeterStrs)
        for i, oneStr in enumerate(PowerMeterStrs):
            cleanStr = oneStr.replace('[', '').replace(']', '')\
                             .replace(',', '').replace('\'', '')\
                             .replace(' ', '').replace('(','')
            PowerMeterCleanStrs[i] = cleanStr

        PowerMeters = \
        [
            [
                (oneMeterStr[0], oneMeterStr[1:]) 
                for oneMeterStr in cleanStr.split(')')[0:-1]
            ] for cleanStr in PowerMeterCleanStrs
        ]

        return zip(buildingIDs, buildingNames, PowerMeters)
