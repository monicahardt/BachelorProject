import csv
import plotly.graph_objects as go
import plotly.io as pio
import emblaze
from gensim.models import Word2Vec
import numpy as np
import csv
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import pacmap
import json
from collections import defaultdict
import re



#model_5000 = Word2Vec.load("../Data/Models/word2vec_epoch_5000.model")
#model_200 = Word2Vec.load("../Data/Models/word2vec_epoch_200_min_1.model")
model_1000 = Word2Vec.load("Data/Models/word2vec_epoch_1000_min_1.model")
#model_3000 = Word2Vec.load("../Data/Models/word2vec_epoch_3000_min_1.model")


import emblaze
from emblaze.utils import Field, ProjectionTechnique

with open('Data/sequences.csv', 'r') as f:
    reader = csv.reader(f)
    sequences = list(reader)
    
address_count_seq = {}
for seq in sequences:
    for place in seq:
        if place in address_count_seq:
            address_count_seq[place] += 1
        else:
            address_count_seq[place] = 1

address_count_seq

def label_function_address_count(labels, station_names): 
    for station_name in station_names:
            # Check if the station_name exists in address_coordinates dictionary
            if station_name in address_count_seq:
                if address_count_seq[station_name] == 1:
                    labels.append(address_count_seq[station_name])
                else: 
                 labels.append("")
            #     labels.append(address_count_seq[station_name])
            # else: 
            #     labels.append("")
    return labels

labels = label_function_address_count([], model_1000.wv.index_to_key)
# Convert labels to numerical format
label_encoder = LabelEncoder()
label_encoder.fit(labels)
numeric_labels = label_encoder.transform(labels)

# X is an n x k array, Y is a length-n array
X, Y = model_1000.wv.vectors, labels

# Represent the high-dimensional embedding
emb = emblaze.Embedding({Field.POSITION: X, Field.COLOR: Y})
# Compute nearest neighbors in the high-D space (for display)
emb.compute_neighbors(metric='cosine')

# Generate UMAP 2D representations - you can pass UMAP parameters to project()
variants = emblaze.EmbeddingSet([
    emb.project(method=ProjectionTechnique.UMAP) for _ in range(10)
])
# Compute neighbors again (to indicate that we want to compare projections)
variants.compute_neighbors(metric='euclidean')

w = emblaze.Viewer(embeddings=variants)
w