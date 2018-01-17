import mod.crawIO as crawIO
import mod.dbUtil as dbUtil

MAPPING_CSV     = 'assets/fixed_mapping.csv'

MappingTuples = crawIO.loadMappingCSV(MAPPING_CSV)
for b_id, b_name, meters in MappingTuples:
    print('Saving mapping of ' + str(b_id) + '\t: ' + str(b_name))
    for m_sign, m_id in meters:
        dbUtil.Mapping.update({
            'BuildingID':       b_id,
            'BuildingName':     b_name
        },{
            "$addToSet": {
                'PowerMeters': {
                    'PowerID':  m_id,
                    'sign':     m_sign
                }
            }
        },
            upsert = True   
        )
print('Done')
