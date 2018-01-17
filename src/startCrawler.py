import mod.crawUtil as crawUtil
import mod.crawIO   as crawIO
import pymongo
import pytz
from pymongo import MongoClient
from datetime import datetime, timedelta

# Constants
POWER_SITE_URL  = 'http://140.112.166.97/power/fn2/dataq.aspx'
METER_CSV    = 'assets/meter.csv'
DATABASE_NAME   = 'Power-database'
START_DATE_STR  = '2013/12/01'
START_DATE      = crawUtil.dateStr2Time(START_DATE_STR, 'd')
END_DATE        = datetime.now()
TAIPEI_TZ       = pytz.timezone('Asia/Taipei')

meterIDs, meterNames = crawIO.loadMetersCSV(METER_CSV)

client      = MongoClient()
PowerDB     = client[DATABASE_NAME]
PowerList   = PowerDB.PowerList      # Collection of Power Meter

def createEmptyData(meter_id, meter_name):
    PowerList.update({
        "PowerID":meter_id,
        "PowerName":meter_name,
        "PowerMonthList":[]
    },{}, upsert = True)

def insertNewMonth(meter_id, meter_name, one_date):
    the_date = TAIPEI_TZ.localize(one_date)
    PowerList.update({
        "PowerID":meter_id,
        "PowerName":meter_name,
    },{
        "$push":{
            "PowerMonthList":{
                "PowerMonth":the_date,
                "PowerDateList":[]
            }
        }    
    }

def insertPowerData(meter_id, meter_name, meter_data, one_date, timeType):
    assert timeType in ['d', 'h', 'n'], \
        'timeType should be (d)ay, (h)our, (n)-min, input is ' + str(timeType)
    the_date    = TAIPEI_TZ.localize(one_date)
    _month      = dateStr2Time(dateTime2Str(the_date, 'm'), 'm')
    _date       = dateStr2Time(dateTime2Str(the_date, 'd'), 'd')
    _hour       = dateStr2Time(dateTime2Str(the_date, 'h'), 'h')
    _time       = dateStr2Time(dateTime2Str(the_date, 't'), 't')
    ##### TODO #####
    if timeType == 'd':
        PowerList.update({
            "PowerID":meter_id,
            "PowerName":meter_name,
            "PowerMonthList.PowerMonth":_month
        },{
            "$push":{
                "PowerMonthList.PowerDateList":{
                    "PowerDate":the_date,
                    "PowerDateAve":{
                        "PowerDateWatt":meter_data
                    }
                }
            }    
        }
    ##### TODO #####


for idx, meter_id in enumerate(meterIDs):
    meter_name = meterNames[idx]
    createEmptyData(meter_id, meter_name)
    for one_date in crawUtil.dateRange(START_DATE, END_DATE):
        one_date_str    = crawUtil.dateTime2Str(one_date, 'd')
        next_date_str   = crawUtil.dateTime2Str(one_date+timedelta(1), 'd')
        for dtype in ['d', 'h', 'n']:
            powerSoup = crawUtil.fetchHTML(
                url     = POWER_SITE_URL,
                meter   = meter_id,
                dt1     = one_date_str,
                dt2     = next_date_str,
                dtype   = dtype
            )
            _, powerData = crawUtil.parsePowerData(powerSoup)
           if dtype != 'n':
               powerData = powerData[0:-1]

