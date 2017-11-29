import mod.crawUtil as crawUtil
import mod.crawIO   as crawIO

# Constants
POWER_SITE_URL  = 'http://140.112.166.97/power/fn2/dataq.aspx'
BUILDING_CSV    = 'assets/meter.csv'
BUILDING_ID     = '00A_P1_01'
DATE_STRING1    = '2017/1/1'
DATE_STRING2    = '2017/1/2'
TYPE_MESSAGE    = ['day', 'hour', '5-min']

for itype, dtype in enumerate(['d','h','n']):
    powerSoup    = crawUtil.fetchHTML(
        url     = POWER_SITE_URL,
        build   = BUILDING_ID,
        dt1     = DATE_STRING1,
        dt2     = DATE_STRING2,
        dtype   = dtype
    ) # BeutifulSoup Object
    powerDataTuple = crawUtil.parsePowerData(powerSoup)
    # ( Attrs, Data )
    buildingTuples = crawUtil.parseBuildings(powerSoup)
    # [(ID, name), ... ]
    print('\n\033[1;33mFetch data of '+BUILDING_ID+' on '+DATE_STRING1+' every '+TYPE_MESSAGE[itype]+'.\033[0m')
    crawIO.printPowerData(powerDataTuple)

crawIO.dumpBuildingsCSV(buildingTuples, BUILDING_CSV)
print('Buildings data is writen in \033[0;36m'+BUILDING_CSV+'\033[0m.')
