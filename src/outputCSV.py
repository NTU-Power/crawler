import pymongo
from pymongo import MongoClient

# constants
DATABASE_NAME   = 'Power-database'
FIELD_FILE      = 'assets/fieldFile.txt'
OUTPUT_CSV      = 'assets/building.csv'

with open(FIELD_FILE) as ff:
    raw_list = ff.readlines()
    fieldList = [a[0:-1] for a in raw_list]


def concatList(inputList):
    outputStr = ''
    if type(inputList[0]) == str:
        for idx, oneStr in enumerate(inputList):
            oneStr = oneStr.replace(',','_')
            outputStr += oneStr if oneStr[0] != ' ' else oneStr[1:]
            outputStr += '_' if idx != len(inputList)-1 else ''

    return outputStr

def all2str(inputObj):
    if type(inputObj) == list:
        return concatList(inputObj)
    else:
        return str(inputObj)

def fields2data(fieldList):

    project_dict = {
        '_id':0
    }
    for oneField in fieldList:
        project_dict[oneField] = 1
        
    dbResult = Colleges.aggregate([
        {"$project":
            project_dict
        }, 
        {"$unwind":"$CollegeBuildingList"},
    ])['result']
    # A list of documents

    resultLines = ['']
    for idx, oneField in enumerate(fieldList):
        resultLines[0] += oneField
        resultLines[0] += ',' if idx != len(fieldList)-1 else ''

    for oneDoc in dbResult:
        resultLine = ''
        for idx, oneField in enumerate(fieldList):
            tmpDoc = oneDoc
            fieldLayers = oneField.split('.')
            for oneLayer in fieldLayers:
                tmpDoc = tmpDoc[oneLayer]
            resultLine += tmpDoc if type(tmpDoc) == str else all2str(tmpDoc)
            resultLine += ',' if idx != len(fieldList)-1 else ''
        resultLines.append(resultLine)

    return resultLines



client      = MongoClient()
PowerDB     = client[DATABASE_NAME]
Colleges    = PowerDB.CollegeList

csvData = fields2data(fieldList)
with open(OUTPUT_CSV, 'w') as of:
    for oneLine in csvData:
        of.write(oneLine+'\n')

print('\nAccording to the field file \033[0;36m'+FIELD_FILE+'\033[0m.')
print('Database data is writen in \033[0;36m'+OUTPUT_CSV+'\033[0m.')
