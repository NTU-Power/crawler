import mod.crawUtil as crawUtil
import mod.crawIO   as crawIO
import mod.dbUtil as dbUtil
import pytz
from datetime import datetime, timedelta
from mod.crawUtil import dateStr2Time, dateTime2Str

# Constants
POWER_SITE_URL  = 'http://140.112.166.97/power/fn2/dataq.aspx'
METER_CSV    = 'assets/meter.csv'
START_DATE_STR  = '2013/12/01'
TAIPEI_TZ       = pytz.timezone('Asia/Taipei')
START_DATE      = dateStr2Time(START_DATE_STR, 'd')
END_DATE        = TAIPEI_TZ.localize(datetime.now())

meterIDs, meterNames = crawIO.loadMetersCSV(METER_CSV)

PowerList   = dbUtil.PowerList      # Collection of Power Meter

def createEmptyData(meter_id, meter_name):
    PowerList.update(
        {
        },
        {
            "PowerID":meter_id,
            "PowerName":meter_name,
            "PowerMonthList":[]
        }, 
        upsert = True
    )

def insertNewMonth(meter_id, meter_name, the_date):
    PowerList.update(
        {
            "PowerID":meter_id,
            "PowerName":meter_name,
        },
        {
            "$addToSet":
            {
                "PowerMonthList":
                {
                    "PowerMonth":the_date,
                    "PowerDateList":[]
                }
            }    
        }
    )

def summaryMonth(meter_id, meter_name, the_date):
    _month      = dateStr2Time(dateTime2Str(the_date, 'm'), 'm')

    onePowerMonth = list(PowerList.find(
        {
            "PowerID":      meter_id,
            "PowerName":    meter_name,
            "PowerMonthList.PowerMonth": _month
        }
    ))
    powerDateList = onePowerMonth[0]['PowerMonthList'][0]['PowerDateList']
    powerMonthWattList = []
    powerMonthUsage = 0
    for powerDateDict in powerDateList:
        powerDateWatt   = powerDateDict['PowerDateData']['PowerDateWatt']
        powerDateUsage  = powerDateDict['PowerDateData']['PowerDateUsage']
        powerMonthWattList.append(powerDateWatt)
        powerMonthUsage += powerDateUsage

    powerMonthWatt = sum(powerMonthWattList)/len(powerMonthWattList)

    PowerList.update(
        {
            "PowerID":      meter_id,
            "PowerName":    meter_name,
            "PowerMonthList.PowerMonth": _month
        },
        {
            "$set":
            {
                "PowerMonthList.$.PowerMonthAve":{
                    "PowerMonthWatt":   powerMonthWatt,
                    "PowerMonthUsage":  powerMonthUsage
                }
            }
        }
    )
    


def insertPowerData(meter_id, meter_name, meter_data, the_date, timeType):
    assert timeType in ['d', 'h', 'n'], \
        'timeType should be (d)ay, (h)our, (n)-min, input is ' + str(timeType)
    # the_date    = TAIPEI_TZ.localize(one_date)
    _month      = dateStr2Time(dateTime2Str(the_date, 'm'), 'm')
    _date       = dateStr2Time(dateTime2Str(the_date, 'd'), 'd')
    _hour       = dateStr2Time(dateTime2Str(the_date, 'h'), 'h')
    _time       = dateStr2Time(dateTime2Str(the_date, 'n'), 'n')
    if timeType == 'd':
        PowerList.update(
            {
                "PowerID":meter_id,
                "PowerName":meter_name,
                "PowerMonthList.PowerMonth":_month
            },
            {
                "$push":
                {
                    "PowerMonthList.$.PowerDateList":
                    {
                        "PowerDate":the_date,
                        "PowerDateData":
                        {
                            "PowerDateWatt" :   meter_data[1],
                            "PowerDateUsage":   meter_data[3],
                            "PowerDateMeter":   meter_data[2],
                            "PowerDatePFactor": meter_data[4],
                            "PowerDateAPower" : meter_data[11],
                            "PowerDateRPower":  meter_data[12],
                            "PowerDateI_r":     meter_data[5],
                            "PowerDateI_s":     meter_data[6],
                            "PowerDateI_t":     meter_data[7],
                            "PowerDateV_rs":    meter_data[8],
                            "PowerDateV_st":    meter_data[9],
                            "PowerDateV_tr":    meter_data[10]
                        }
                    }
                }    
            }
        )
    elif timeType == 'h':
        PowerList.update(
            {
                "PowerID":meter_id,
                "PowerName":meter_name,
                "PowerMonthList.PowerMonth":_month,
                "PowerMonthList.PowerDateList.PowerDate":_date
            },
            {
                "$push":
                {
                    "PowerMonthList.0.PowerDateList.$.PowerHourList":
                    {
                        "PowerHour":the_date,
                        "PowerHourData":
                        {
                            "PowerHourWatt" :   meter_data[1],
                            "PowerHourUsage":   meter_data[3],
                            "PowerHourMeter":   meter_data[2],
                            "PowerHourPFactor": meter_data[4],
                            "PowerHourAPower" : meter_data[11],
                            "PowerHourRPower":  meter_data[12],
                            "PowerHourI_r":     meter_data[5],
                            "PowerHourI_s":     meter_data[6],
                            "PowerHourI_t":     meter_data[7],
                            "PowerHourV_rs":    meter_data[8],
                            "PowerHourV_st":    meter_data[9],
                            "PowerHourV_tr":    meter_data[10]
                        }
                    }
                }    
            }
        )
    elif timeType == 'n':
        PowerList.update(
            {
                "PowerID":meter_id,
                "PowerName":meter_name,
                "PowerMonthList.PowerMonth":_month,
                "PowerMonthList.PowerDateList.PowerDate":_date,
                "PowerMonthList.PowerDateList.PowerDate.PowerHour":_hour
            },
            {
                "$push":
                {
                    "PowerMonthList.0.PowerDateList.0.PowerHourList.$.PowerTimeList":
                    {
                        "PowerTime":the_date,
                        "PowerTimeData":
                        {
                            "PowerTimeWatt" :   meter_data[1],
                            "PowerTimeUsage":   meter_data[3],
                            "PowerTimeMeter":   meter_data[2],
                            "PowerTimePFactor": meter_data[4],
                            "PowerTimeAPower" : meter_data[11],
                            "PowerTimeRPower":  meter_data[12],
                            "PowerTimeI_r":     meter_data[5],
                            "PowerTimeI_s":     meter_data[6],
                            "PowerTimeI_t":     meter_data[7],
                            "PowerTimeV_rs":    meter_data[8],
                            "PowerTimeV_st":    meter_data[9],
                            "PowerTimeV_tr":    meter_data[10]
                        }
                    }
                }    
            }
        )

# Main Function

for idx, meter_id in enumerate(meterIDs):
    meter_name = meterNames[idx]
    createEmptyData(meter_id, meter_name)
    for one_date in crawUtil.dateRange(START_DATE, END_DATE):
        one_date_str    = dateTime2Str(one_date, 'd')
        next_date_str   = dateTime2Str(one_date+timedelta(1), 'd')

        print('Start processing '+one_date_str)

        # insert if the date == 1st
        if one_date_str[-2:] == '01':
            print('Add new month: '+one_date_str[0:-3]) 
            insertNewMonth(meter_id, meter_name, one_date)

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

            for meter_data in powerData:
                if dtype == 'd':
                    one_datetime = dateStr2Time(meter_data[0], dtype)
                if dtype == 'h':
                    one_datetime = dateStr2Time(meter_data[0][0:-3], dtype)
                if dtype == 'n':
                    one_datetime = dateStr2Time(meter_data[0], dtype)
                insertPowerData(
                    meter_id, 
                    meter_name, 
                    meter_data, 
                    one_datetime,
                    dtype
                )
            
        # summary if next date == 1st
        if next_date_str[-2:] == '01':
            summaryMonth(meter_id, meter_name, one_date)
            print('Summary month: '+one_date_str[0:-2]) 
