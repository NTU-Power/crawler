import mod.crawUtil as crawUtil
import mod.crawIO   as crawIO

# Constants
POWER_SITE_URL  = 'http://140.112.166.97/power/fn2/dataq.aspx'
METER_CSV       = 'assets/meter.csv'
METER_ID        = '00A_P1_01'
DATE_STRING1    = '2017/1/1'
DATE_STRING2    = '2017/1/2'
TYPE_MESSAGE    = ['day', 'hour', '5-min']

for itype, dtype in enumerate(['d','h','n']):
    powerSoup   = crawUtil.fetchHTML(
        url     = POWER_SITE_URL,
        meter   = METER_ID,
        dt1     = DATE_STRING1,
        dt2     = DATE_STRING2,
        dtype   = dtype
    ) # BeutifulSoup Object
    powerDataTuple = crawUtil.parsePowerData(powerSoup)
    # ( Attrs, Data )
    meterTuples = crawUtil.parseMeters(powerSoup)
    # [(ID, name), ... ]
    print('\n\033[1;33mFetch data of '+METER_ID+' on '+DATE_STRING1+' every '+TYPE_MESSAGE[itype]+'.\033[0m')
    crawIO.printPowerData(powerDataTuple)

crawIO.dumpMetersCSV(meterTuples, METER_CSV)
print('Meters data is writen in \033[0;36m'+METER_CSV+'\033[0m.')
