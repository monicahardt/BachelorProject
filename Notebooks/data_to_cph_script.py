import pandas as pd

data = pd.read_csv('../Data/All_Journeys.csv')
data = data.drop(columns=['JourneyClasses_Id', 'TravelType', 'ExtraFrom', 'ExtraTo', 'Type', 'StartZone', 'StartStop', 'EndStop']).reset_index()

condition_1_cph = (
    (data['internalValidZones'].str.match(r'^(1001|1002|1003|1004)(,(1001|1002|1003|1004))*$')
    | # or
    pd.isna(data['internalValidZones']))
    )

condition_2_cph = (
    (data['internalStartZones'].str.match(r'^(1001|1002|1003|1004)$'))
    | # or
    pd.isna(data['internalStartZones'])
    )


cph_data = data[(condition_1_cph)]
cph_data = cph_data[(condition_2_cph)]

cph_data = cph_data[ ~ (cph_data['SearchStart'].str.contains("okation", na=False)
                                             | #Or
                                             cph_data['SearchStart'].str.contains("zoner", na=False))]
cph_data = cph_data[( ~ (cph_data['SearchEnd'].str.contains("zoner", na=False) 
                                            | #Or
                                            cph_data['SearchEnd'].str.contains("okation", na=False)))]

# next two filters are English filters of the first
cph_data = cph_data[( ~ (cph_data['SearchEnd'].str.contains("zones", na=False) 
                                            | #Or
                                            cph_data['SearchEnd'].str.contains("ocation", na=False)))]

cph_data = cph_data[( ~ (cph_data['SearchStart'].str.contains("zones", na=False) 
                                            | #Or
                                            cph_data['SearchStart'].str.contains("ocation", na=False)))]

# Next filter is to remove entries where one of the matching search-x or x-stop are Null
cph_data = cph_data[( ~ (pd.isna(cph_data['SearchStart'])) & ~ (pd.isna(cph_data['SearchEnd'])))]

# Next filter removes all entries where SearchStart and SearchEnd contain the same value
cph_data = cph_data[(
                        ~(cph_data['SearchStart'] == cph_data['SearchEnd'])
                        )]


cph_data = cph_data.drop(columns=['internalStartZones', 'internalValidZones']).reset_index()


cph_data.to_csv("cph_file.csv", index=False)