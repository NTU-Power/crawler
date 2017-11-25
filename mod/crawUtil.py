import requests
import time
import datetime
import json
from bs4 import BeautifulSoup

def fetchHTML(url, build, dt1, dt2, dtype='n'):
    payload = {
        'dtype': dtype,
        'build': build,
        'dt1'  : dt1,
        'dt2'  : dt2
    }
    res = requests.post(url, payload)
    return BeautifulSoup(res.text, 'lxml')

def parsePowerData(powerSoup):
    powerTables = powerSoup.findAll('table')
    powerTable = powerTables[1]
    powerTableRows = powerTable.findAll('tr')
    powerTableHead = powerTableRows[0]
    powerTableBody = powerTableRows[1:]
    powerTableHeadColms = powerTableHead.findAll('td')
    powerAttrs = []
    powerData = []

    for td in powerTableHeadColms:
        powerAttrs.append(td.text.replace('\xa0', ''))

    for tr in powerTableBody:
        powerDataItem = []
        for idx, td in enumerate(tr.findAll('td')):
            val = td.text.strip()
            if (idx == 0):
                # date column => convert to unix timestamp
                # val = time.mktime(datetime.datetime.strptime(val, "%Y/%m/%d %H:%M").timetuple())
                pass 
            elif (val == '---'):
                val = -1
            else:
                val = float(val)
            powerDataItem.append(val)
        powerData.append(powerDataItem)
    
    return (powerAttrs, powerData)

def parseBuildings(powerSoup):
    buildSelects    = powerSoup.findAll('select')
    buildSelect     = buildSelects[1]
    buildOptions    = buildSelect.findAll('option')

    buildTuples = []
    for buildOption in buildOptions:
        buildTuples.append(
            (buildOption['value'], buildOption.text[len(buildOption['value']):])
        )

    return buildTuples
