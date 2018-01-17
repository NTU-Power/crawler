import pymongo
from pymongo import MongoClient

DATABASE_NAME   = 'Power-database'

client      = MongoClient()
PowerDB     = client[DATABASE_NAME]

CollegeList = PowerDB.CollegeList
PowerList   = PowerDB.PowerList
Mapping     = PowerDB.Mapping
