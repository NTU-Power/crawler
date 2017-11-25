import pymongo
from pymongo import MongoClient

# constants
DATABASE_NAME   = 'Power-database'
COLLECTION_NAME = ''
BUILDING_CSV    = 'assets/buildings.csv'

# get buildingList
buildingList = []
with open(BUILDING_CSV) as csvFile:
    csvLines = csvFile.readlines()[1:] # Except the header line
    for oneLine in csvLines:
        oneList = oneLine.replace('\n','').split(',')
        oneDict = {"BuildingName":oneList[1], "BuildingID":oneList[0]}
        buildingList.append(oneDict)

client      = MongoClient()
PowerDB     = client[DATABASE_NAME]
Colleges    = PowerDB.CollegeList
Colleges.insert_one({
    "CollegeName":'Unknown',
    "CollegeBuildingList":buildingList
})
print('BuildingList has been \033[1;33minserted into MongoDB\033[0m.')
