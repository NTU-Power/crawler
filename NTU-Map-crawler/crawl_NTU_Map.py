import requests
import json
import pymongo
import mod.dbUtil as dbUtil
from bs4 import BeautifulSoup

# constants

URL_LEFT_MENU = 'https://map.ntu.edu.tw/ntu.htm?action=getDepatments'
URL_GET_UID   = 'https://map.ntu.edu.tw/ntu.htm?action=getUid'
URL_GET_MAP   = 'https://map.ntu.edu.tw/geoserver/wfs?'
URL_GET_INFO  = 'https://map.ntu.edu.tw/ntu.htm'

def getLeftMenu():
    payload = {
        'locale':'tw'
    }
    res = requests.post(URL_LEFT_MENU, payload)
    leftMenu = json.loads(res.text)
    return leftMenu['maplist']

def getUIDfromName(name, typeID):
    payload = {
        'type':typeID,
        'query':name,
        'locale':'tw'
    }
    res = requests.post(URL_GET_UID, payload)
    return json.loads(res.text)['data']

def getMapFromUID(uidList):
    coordListForUIDs = []
    for oneUID in uidList:
        uid_query_string = 'uid=\'' + oneUID +'\''

        payload = {
            'service':'WFS',
            'version':'1.0.0',
            'request':'GetFeature',
            'typename':'gips:ntu_building_bound',
            'CQL_FILTER':uid_query_string
        }

        res = requests.get(URL_GET_MAP, payload)
        coordList = [a.text for a in BeautifulSoup(res.text, 'xml').findAll('gml:coordinates')]

        wgsList = []
        for coordStr in coordList:
            oldPointList = coordStr.split(' ')
            newPointList = []
            for oneOldPoint in oldPointList:
                oldPointList = oneOldPoint.split(',')
                newX, newY = TWD2WGS(float(oldPointList[0]), float(oldPointList[1]))
                newPointList.append([newX,newY])
            wgsList.append(newPointList)
        coordListForUIDs.append(wgsList)

    return coordListForUIDs

def getInfoFromUID(uidList, typeStr='build'):
    infoList = []
    for uid in uidList:
        payload = {
            'type':typeStr,
            'uid':uid,
            'id':'ext-gen1',
            'buildid':''
        }
        res = requests.post(URL_GET_INFO, payload)
        resDict = json.loads(res.text)

        nameList = []
        if resDict['fdata'] != None and resDict['fdata']['nickname'] != '':
            nicknameStr = resDict['fdata']['nickname']
            nameList = nicknameStr.split(';')
        else:
            nameList = [resDict['buildingBound']['name']]
        if '' in nameList:
            nameList.remove('')

        if 'buildingBound' not in resDict.keys() or resDict['buildingBound']['area'] == '':
            infoList.append({'name':nameList})
            continue
        oneInfo = {
            'name':nameList,
            'area':float(resDict['buildingBound']['area'].replace(',','')),
            'floor':int(resDict['buildingBound']['floor']),
            'basement':int(resDict['buildingBound']['basement'])
        }
        infoList.append(oneInfo)

    return infoList

def TWD2WGS(TWDx, TWDy):
    TWD1 = (302365.188, 2770374.856)
    TWD2 = (305192.412, 2767499.179)
    WGS1 = (121.518941, 25.040600)
    WGS2 = (121.546843, 25.014538)
    xSlope = (WGS2[0]-WGS1[0])/(TWD2[0]-TWD1[0])
    ySlope = (WGS2[1]-WGS1[1])/(TWD2[1]-TWD1[1])
    WGSx = (TWDx-TWD1[0])*xSlope + WGS1[0]
    WGSy = (TWDy-TWD1[1])*ySlope + WGS1[1]
    return (WGSx, WGSy)

def insertBuilding(
    collegeName,
    buildingUIDs,
    buildingInfo,
    buildingCoord
):
    
    for idx, uid in enumerate(buildingUIDs):
        try:
            oneBuilding = {
                'BuildingNames':    buildingInfo[idx]['name'],
                'BuildingID':       uid,
                'BuildingArea':     buildingInfo[idx]['area'],
                'BuildingLocation': {
                    'type':         "MultiPolygon",
                    'coordinates':  buildingCoord[idx]
                },
                'BuildingFloors': {
                    'floor':        buildingInfo[idx]['floor'],
                    'basement':     buildingInfo[idx]['basement']
                }
            }
        except KeyError:
            print('\033[0;31mKeyError\033[0m: Fail to get ' + buildingInfo[idx]['name'][0])
            continue

        Colleges.update({
            'CollegeName':collegeName
        },
        {
            "$addToSet": {
                'CollegeBuildingList':oneBuilding
            }
        },
            upsert=True
        )

Colleges    = dbUtil.CollegeList

print('\n\nStart to load data into mongoDB: \033[0;36mPower-database\033[0m.')
menuList = getLeftMenu()
for oneMenu in menuList:
    theTypeID = oneMenu['type']
    collegeName = oneMenu['main']
    for oneName in oneMenu['sub']:
        if oneName == None or oneName == '':
            continue
        uidList = getUIDfromName(oneName, theTypeID)
        infoList = getInfoFromUID(uidList)
        coordList = getMapFromUID(uidList)
        assert(len(infoList) == len(uidList))
        assert(len(coordList) == len(uidList))

        if collegeName == '學術單位':
            print(oneName, *uidList)
            insertBuilding(oneName, uidList, infoList, coordList)
        else:
            print(collegeName, oneName, *uidList)
            insertBuilding(collegeName, uidList, infoList, coordList)

