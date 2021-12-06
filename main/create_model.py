import csv
import pickle
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

df_data = pd.read_csv('filtered_dataset.csv')
df_data.index = df_data.iloc[:, 0]
df_data.index.name = "userID"
df_data = df_data.drop(df_data.columns[0], axis=1)
df_data.columns.name = "movieID"
df_data = df_data.transpose()
mat_data = csr_matrix(df_data.values)
with open("mat_data.pickle", "wb") as file:
    pickle.dump(mat_data, file)

model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model_knn.fit(mat_data)
with open("model_knn.pickle", "wb") as file:
    pickle.dump(model_knn, file)

movie_indices = list(df_data.index)
tmp = []
for movie_index in movie_indices:
    tmp.append(int(movie_index))
movie_indices = tmp

title_to_index = {}
with open("movie_titles.csv", "r") as f:
    r = csv.reader(f)
    for row in r:
        movieID = int(row[0])
        movie_title = row[2]
        try:
            movie_index = movie_indices.index(movieID)
            title_to_index[movie_title] = movie_index
        except ValueError:
            pass
with open("title_to_index.pickle", "wb") as file:
    pickle.dump(title_to_index, file)
