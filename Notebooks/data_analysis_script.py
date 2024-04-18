# %%
import pandas as pd
import os
from collections import Counter
import glob
from tqdm.notebook import tqdm
from gensim.models import word2vec
import collections
from scipy.stats import entropy
import sklearn
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from itertools import combinations
import umap
import pacmap
import numpy as np
from scipy.spatial import ConvexHull
from numpy.linalg import norm
from numpy import dot
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy
import warnings
import re
import json
import csv

# %%
model=word2vec.Word2Vec.load('../Data/Models/word2vec_epoch_1000_min_1.model')

# %%
f = open('../Data/data.json')
data = json.load(f)

a = open('../Data/added_data.json')
added_data = json.load(a)

# %%
X = model.wv.vectors

# %%
with open('../Data/sequences.csv', 'r') as f:
    reader = csv.reader(f)
    sequences = list(reader)

# %%
# tsne
def tsne_plot(X):
    X=np.array(X)
    #pca = PCA(n_components=50)
    #X_pca=pca.fit_transform(X)
    proj = TSNE().fit_transform(X)
    return proj
proj=tsne_plot(X)

# UMAP 
proj_1 = umap.UMAP(n_components=2, metric='cosine').fit_transform(X)

# pca 
pca = PCA(n_components=2)
proj_2=pca.fit_transform(X)

# %%
# pacmap 
embedding = pacmap.PaCMAP(n_components=2, n_neighbors=None, MN_ratio=0.5, FP_ratio=2.0) 
proj_3 = embedding.fit_transform(X, init="pca")


# %% [markdown]
# get list of unique zipcodes

# %%
zips = {}

# %%
import re
#retrieve zipcode
def getZip(info):
    pattern = '\d{4}'
    match = re.search(pattern, info)
    if match is not None:
        return match.group()
    else :
        return

def add_to_dict(zip_code):
    if str.startswith(zip_code,'1'):
        zip_code = '1000'
    #check if it is already in the dictionary
    if zip_code in zips:
        zips[zip_code] += 1
    else:
        zips[zip_code] = 1
    return zip_code

# # Extract zip codes 
address_zips = {}
wrong_addresses = []
# we have some json objects where the address exists but the info is null. This happens in 1602 cases (assume this is where the geolocator failed)
for address, info in data.items():
    if info is not None: 
        zip_code = getZip(info['address'])  # Extract zip code from address could be empty
        if zip_code is not None:
            if 1000 <= int(zip_code) < 4999: #for now removing all failed zipcodes in Jylland
                #get list of unique zipcodes
                zip = add_to_dict(zip_code)
                address_zips[address] = zip
            else: 
                wrong_addresses.append(address) #go through later
        else:
            address_zips[address] = 0000 #no zipcode was found
    else:
        address_zips[address] = 0000 #no info was found on the address?

#run through the list of wrong addresses and try to find them in the added_data.json file to get the "correct" zipcode
for address in wrong_addresses:
    #find in json file
    if address in added_data:
        zip = getZip(added_data[address]['address'])
        address_zips[address] = zip

for address, zip_code in address_zips.items():
    print(address)
    print(zip_code)
    print()

print(len(address_zips))

# %%
print(zips)

# %%
fig, ax = plt.subplots(2,2, figsize=(12,10))
palette = ['tab:green','tab:orange','tab:blue','tab:red','tab:purple']
xs=[proj_2, proj, proj_1, proj_3]
ts=["PCA","t-SNE","UMAP", "PaCMAP"]
s=0
for row in ax:
    for col in row:
        m=0
        for n in journal_fields.Field.unique():
            col.set_title(ts[s], fontsize=25)
            j1=journal_fields[journal_fields.Field==n].VenueId
            col.scatter([xs[s][tokens_idx[i]][0] for i in j1],[xs[s][tokens_idx[i]][1] for i in  j1], lw=0.1, s=5, edgecolors='white', label=n, c=palette[m])
            m+=1
        s+=1
        col.axis('off')
plt.legend()
fig.tight_layout()
#plt.savefig('label.png',  bbox_inches='tight')
plt.show()

# %%
import matplotlib.pyplot as plt

# Define color palette for zip codes
zip_colors = {}  # Dictionary to map zip codes to colors
unique_zip_codes = set(address_zips.values())
num_colors = len(unique_zip_codes)
color_palette = plt.cm.get_cmap('tab20', num_colors)  # Choose a colormap

for idx, zip_code in enumerate(unique_zip_codes):
    zip_colors[zip_code] = color_palette(idx)

# Create the plot for t-SNE only
fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the figure size as needed

# Set the title for t-SNE plot
ax.set_title("t-SNE", fontsize=25)

for zip_code in unique_zip_codes:
    # Filter data based on zip code
    journeys_with_zip = [journey for journey, zip_code_journey in address_zips.items() if zip_code_journey == zip_code]
    ax.scatter(
        [proj[idx][0] for idx, journey in enumerate(sequences) if journey in journeys_with_zip],
        [proj[idx][1] for idx, journey in enumerate(sequences) if journey in journeys_with_zip],
        lw=0.1, s=5, edgecolors='white',
        label=zip_code, c=zip_colors[zip_code]
    )

# Create a custom legend
handles = [plt.Line2D([0], [0], marker='o', color='w', markersize=10, markerfacecolor=zip_colors[zip_code], label=zip_code) for zip_code in unique_zip_codes]
ax.legend(handles=handles, title='Zip Code')

ax.axis('off')  # Turn off the axis for cleaner plot

plt.tight_layout()
plt.show()


# %%



