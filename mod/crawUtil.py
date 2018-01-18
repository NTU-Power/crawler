import requests
import time
import datetime
import json
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TAIPEI_TZ       = pytz.timezone('Asia/Taipei')

def fetchHTML(url, meter, dt1, dt2, dtype='n'):
    payload = {
        'dtype': dtype,
        'meter': meter,
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

def parseMeters(powerSoup):
    meterSelects    = powerSoup.findAll('select')
    meterSelect     = meterSelects[1]
    meterOptions    = meterSelect.findAll('option')

    meterTuples = []
    for meterOption in meterOptions:
        meterTuples.append(
            (meterOption['value'], meterOption.text[len(meterOption['value']):])
        )

    return meterTuples

def _timeType2Format(timeType):
    assert timeType in ['m', 'd', 'h', 'n'], \
        'timeType should be (m)onth, (d)ay, (h)our, (n)-min, input is ' + str(timeType)
    _format = '%Y/%m'
    if timeType == 'd':
        _format += '/%d'
    elif timeType == 'h':
        _format += '/%d %H'
    elif timeType == 'n':
        _format += '/%d %H:%M'
    return _format

def dateStr2Time(inputStr, timeType):
    _format = _timeType2Format(timeType)
    _datetime = datetime.strptime(inputStr, _format)
    return TAIPEI_TZ.localize(_datetime)

def dateTime2Str(inputTime, timeType):
    _format = _timeType2Format(timeType)
    return datetime.strftime(inputTime, _format)

def dateRange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

