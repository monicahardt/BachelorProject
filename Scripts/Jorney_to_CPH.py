import pandas as pd


def load_data(path):
    return pd.read_csv(path)


def filter_cph_zones(data):
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
    return cph_data

def filter_valid_entries(cph_data):
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
    cph_data = cph_data[(
                                            ( ~ (pd.isna(cph_data['SearchStart'])) & ~ (pd.isna(cph_data['SearchEnd'])))
                                            | # Or
                                            ( ~ (pd.isna(cph_data['StartStop'])) & ~ (pd.isna(cph_data['EndStop'])))
                                            )]

    # Next filter removes all entries where SearchStart and SearchEnd contain the same value
    cph_data = cph_data[(
                            ~(cph_data['SearchStart'] == cph_data['SearchEnd'])
                            )]

    return cph_data

def save_cph_data_csv(data) -> None:
    data.to_csv('Data/cph_file_test.csv')


def tests(cph_data):
    # Test 1 for whether our data contain seachEnd with contains 'lokation' or 'location'
    lokation_count = cph_data[cph_data['SearchEnd'].str.contains("okation", na=False)].count()
    print(f"Amount of 'Lokation' entires in 'SearchEnd' : {lokation_count['SearchEnd']}")

    location_count = cph_data[cph_data['SearchEnd'].str.contains("ocation", na=False)].count()
    print(f"Amount of 'Location' entires in 'SearchEnd' : {location_count['SearchEnd']}")

    # Test 2 for whether our data contain seachStart with contains 'lokation' or 'location'
    lokation_count_s = cph_data[cph_data['SearchStart'].str.contains("okation", na=False)].count()
    print(f"Amount of 'Lokation' entires in 'SearchStart' : {lokation_count_s['SearchStart']}")

    location_count_s = cph_data[cph_data['SearchStart'].str.contains("ocation", na=False)].count()
    print(f"Amount of 'Location' entires in 'SearchStart' : {location_count_s['SearchStart']}")

    # Test 3 for whether our data contain SearchStart with 'zones' or 'zoner'
    zones_count = cph_data[cph_data['SearchEnd'].str.contains("zones", na=False)].count()
    print(f"Amount of 'zones' entires in 'SearchEnd' : {zones_count['SearchEnd']}")

    zones_count_r = cph_data[cph_data['SearchEnd'].str.contains("zoner", na=False)].count()
    print(f"Amount of 'zoner' entires in 'SearchEnd' : {zones_count_r['SearchEnd']}")

    # Test 4 for whether our data contain None in 3 or more fields (startStop, EndStop, SearchStart and SearchEnd)
    num_nulls = cph_data[['StartStop', 'EndStop', 'SearchStart', 'SearchEnd']].isna().sum(axis=1)
    b = (num_nulls >= 3).any()
    print(f"Does the data contain a row which 3 of StartStop, EndStop, SearchStart or SearchEnd is null: {b}")

    # Test 5 for whether our data contain duplicates in matching fields, i.e. StartStop == EndStop
    duplicates_in_stop = cph_data[(cph_data['StartStop'] == cph_data['EndStop'])].count()
    print(f"Amount of matching values in StartStop and EndStop : {duplicates_in_stop['StartStop']}")


    # Test 6 for whether our data contain duplicates in matching fields, i.e. SearchStart == SearchEnd
    duplicates_in_stop = cph_data[(cph_data['SearchStart'] == cph_data['SearchEnd'])].count()
    print(f"Amount of matching values in SearchStart and SearchEnd : {duplicates_in_stop['SearchStart']}")

    # Test 7 for whether our data contain three of the fields filled.
    num_filled = ~(cph_data[['StartStop', 'EndStop', 'SearchStart', 'SearchEnd']].isna()).sum(axis=1)
    b = (num_filled == 3).any()
    print(f"Does the data contain a row which 3 of StartStop, EndStop, SearchStart or SearchEnd are filled: {b}")
    


def main():
    PATH = 'Data/All_Journeys.csv'
    data = load_data(PATH)
    data = filter_cph_zones(data)
    data = filter_valid_entries(data)
    save_cph_data_csv(data)
    

main()
