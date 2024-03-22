# %% [markdown]
# # Welcome to the Notebook for Monha's and Bemi's Bachelor Project
# 
# ## Content
# 
# In this notebook we will:
# 
# 1. Aggrigate our data into usable travel sequences with only the relevant data 
# 2. Analyse the appropriate data
# 3. Create an embedding space using Word2Vec
# 
# We will use the following format for the structure of the file:
# 1. MD file to describe the intention of the following code followed by an explanation of the results from the code if any
# 2. Code block to write code

# %% [markdown]
# # Initial Setup
# 
# Please pip install the correct libraries for the following code to work.

# %%
%pip install pandas # Pandas for data handling
%pip install numpy  # Maths stuff

# %%
import pandas as pd
import numpy as np

# %% [markdown]
# # Data import
# 
# The data used in this notebook is extracted from the Journeys table from the DB. 
# 
# The data in question contains ~43 mil rows. This data is all journeys traveled in the timespan of ~4 years. For the purpose of this project we wish to filter the data, such that we only work with journeys within Copenhagen.

# %%
data = pd.read_csv('../Data/All_Journeys.csv')
data

# %% [markdown]
# ## Filtering data
# 
# In order to filter our data, XXX checks need to be made to be certain a journey is within cph as well as containing information relevant for our purpose. 
# 
# For a journey to be within cph they need to only make use of zone 1 through 4
# 1. Check if *internalStartZones* only contain zones within cph
# 2. Check if *internalValidZones* only contain zones within cph
# 
# For a journey to be relevant for the project, we need the fields *StartStop*, *EndStop*, *SearchStart* and *SearchEnd* to be either fully filled out or partly - that is, if Start- and EndStop are null, then SearchStart and -End need to be filled. Likewise, the fields must not match in their values; a journeys start and end should not be the same.
# 

# %%
#Copenhagen filtering
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

# %%
cph_data_1 = data[(condition_1_cph)]
cph_data_2 = cph_data_1[condition_2_cph]

cph_data_3 = cph_data_2[ ~ (cph_data_2['SearchStart'].str.contains("okation", na=False)
                                             | #Or
                                             cph_data_2['SearchStart'].str.contains("zoner", na=False))]
cph_data_4 = cph_data_3[( ~ (cph_data_3['SearchEnd'].str.contains("zoner", na=False) 
                                            | #Or
                                            cph_data_3['SearchEnd'].str.contains("okation", na=False)))]

# next two filters are English filters of the first
cph_data_5 = cph_data_4[( ~ (cph_data_4['SearchEnd'].str.contains("zones", na=False) 
                                            | #Or
                                            cph_data_4['SearchEnd'].str.contains("ocation", na=False)))]

cph_data_6 = cph_data_5[( ~ (cph_data_5['SearchStart'].str.contains("zones", na=False) 
                                            | #Or
                                            cph_data_5['SearchStart'].str.contains("ocation", na=False)))]

# Next filter is to remove entries where one of the matching search-x or x-stop are Null
cph_data_7 = cph_data_6[(
                                        ( ~ (pd.isna(cph_data_6['SearchStart'])) & ~ (pd.isna(cph_data_6['SearchEnd'])))
                                        | # Or
                                        ( ~ (pd.isna(cph_data_6['StartStop'])) & ~ (pd.isna(cph_data_6['EndStop'])))
                                        )]

# Next filter removes all entries where SearchStart and SearchEnd contain the same value
cph_data = cph_data_7[(
                        ~(cph_data_7['SearchStart'] == cph_data_7['SearchEnd'])
                        )]

cph_data

# %%
cph_data = data[(condition_1_cph)]
cph_data = cph_data[condition_2_cph]

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

cph_data

# %% [markdown]
# ## Testing to see whether our filtering worked
# 
# Since we are handling a very large amount of data, it can be difficult to scim through the data in order to see if it is as intended. These tests are used in order to detect whether or not rows that are not supposed to be in our data is in our data.

# %%
# Test 1 for whether our data contain seachEnd with contains 'lokation' or 'location'
lokation_count = cph_data[cph_data['SearchEnd'].str.contains("okation", na=False)].count()
print(f"Amount of 'Lokation' entires in 'SearchEnd' : {lokation_count['SearchEnd']}")

location_count = cph_data[cph_data['SearchEnd'].str.contains("ocation", na=False)].count()
print(f"Amount of 'Location' entires in 'SearchEnd' : {lokation_count['SearchEnd']}")

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


# %% [markdown]
# # From ID to Station
# 
# We wish to get rid of the IDs used in StartStop and EndStop as these do not really give us a direct understanding of what station is used in a journey. Therefore we will use the table SJWaypoints to match a given Station-Id with a 'Name'. We then wish replace all the entries in our cph_data such that we do not have these integers as IDs but rather a stop-name. 

# %%
id_to_name_data = pd.read_csv('../Data/SJ_results.csv')
grouped_id_name = id_to_name_data[['Id', 'Name']].groupby('Id')

# %%
grouped_id_name.value_counts()
id_name_list = grouped_id_name.agg(list)

id_to_name_dict = {}

for id, frame in grouped_id_name:
    if id not in id_to_name_dict:
        id_to_name_dict[id] = frame['Name'].iloc[0]


# %% [markdown]
# ## Change of cph_data
# 
# We now wish to replace all Ids in cph_data from StartStop and EndStop with the associated Name from the dict. 

# %%
test_df = cph_data

# %%
def id_to_station(row):
    if pd.notna(row['StartStop']) : 
        row['StartStop'] = id_to_name_dict[row['StartStop']]
        row['EndStop'] = id_to_name_dict[row['EndStop']]
    return row

test_df = test_df.apply(id_to_station, axis=1)
        

# %% [markdown]
# # Sequences
# 
# We now wish to make sequences from the journeys. The sequnces should either be a value pair of SearchStart and Searchend or a pair of StartStop and EndStop. To do this we simply collect the pairs from the dataframe where StartStop and EndStop Id's are "translated" to station names. 
# 
# When making the sequences, certain questions arrise about the data. For instance, of the 3,4 mil datapoints, only 64 of the datapoints contain a value *only* in StartStop and EndStop. (```python test_df[~(pd.isna(test_df['StartStop'])) & (pd.isna(test_df['SearchStart']))]```)
# 
# Another important decision is deciding on how to extract stations from SearchStart and SearchEnd, since a lot of the entries does not consist of a directly matching station. i.e. 'Hovedebanegården' being the SearchStart for the station 'København H'. Thus we need to match these inconsistent strings with a consistent naming convention. 
# 
#

# %%
import re

pattern = r' (\d\d)'

sequences = []

def get_sequence(row) -> None:
    if (pd.isna(row['StartStop'])):
        start   = re.sub(pattern, "", row['SearchStart'])
        end     = re.sub(pattern, "", row['SearchEnd'])
        sequences.append([start, end])
    else:
        start   = re.sub(pattern, "", row['StartStop'])
        end     = re.sub(pattern, "", row['EndStop'])
        sequences.append([start, end])

test_df.apply(get_sequence, axis=1)

# %%
sequences

