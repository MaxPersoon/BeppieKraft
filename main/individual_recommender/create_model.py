import math
import os
import csv
import pickle
import pandas as pd
from numpy import mean, std
from pandas import concat
from scipy.sparse import csr_matrix, vstack
from sklearn.datasets import make_multilabel_classification
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier

os.chdir(os.getcwd().replace('\\individual_recommender', ''))
df_data = pd.read_csv('dataset\\full_dataset.csv')
df_data.index = df_data.iloc[:, 0]
df_data = df_data.drop(df_data.columns[0], axis=1)
mat_data = csr_matrix(df_data.values)
os.remove('individual_recommender\\mat_data.pickle')
with open("individual_recommender\\mat_data.pickle", "wb") as file:
    pickle.dump(mat_data, file)


X = mat_data
y = df_data.iloc[:, 0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

Xfolds = []
yfolds = []

rmseList = []
for i in range(5):
    Xfolds.append(X_train[i*6536:(i+1)*6536, :])
    yfolds.append(y_train[i*6536:(i+1)*6536])

for i in range(5):
    xframe = Xfolds[i]
    yframe = yfolds[i]
    xhold = Xfolds[(i+1)%5]
    yhold = yfolds[(i+1)%5]
    for j in range(5):
        if j != (i+1)%5 and j != i:
            xframe = vstack((xframe,Xfolds[j]))
            yframe = concat([yframe,yfolds[j]])

    model_knn = KNeighborsClassifier(metric='cosine', algorithm='brute', n_neighbors=2, n_jobs=-1)
    model_knn.fit(xframe, yframe)
    pred_y = model_knn.predict(xhold)
    mse = mean_squared_error(yhold, pred_y)
    rmse = math.sqrt(mse)
    print("Root Mean Squared Error:", rmse)
    rmseList.append(rmse)

print(mean(rmseList))

model_knn = KNeighborsClassifier(metric='cosine', algorithm='brute', n_neighbors=2, n_jobs=-1)
model_knn.fit(X_train, y_train)
pred_y = model_knn.predict(X_test)
mse = mean_squared_error(y_test, pred_y)
rmse = math.sqrt(mse)
print("Root Mean Squared Error:", rmse)


# X = mat_data
# y = df_data.iloc[:,0]
# cv = KFold(n_splits=10)
# model_knn = KNeighborsClassifier(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
# scores = cross_val_score(model_knn, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
# print('Accuracy: %.3f (%.3f)' % (mean(scores), std(scores)))
# model_knn.fit(X,y)


model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=1, n_jobs=-1)
model_knn.fit(mat_data)

os.remove('individual_recommender\\model_knn.pickle')
with open("individual_recommender\\model_knn.pickle", "wb") as file:
    pickle.dump(model_knn, file)

movie_indices = list(df_data.index)
tmp = []
for movie_index in movie_indices:
    tmp.append(int(movie_index))
movie_indices = tmp

title_to_index = {}
with open("dataset\\movie_titles.csv", "r") as f:
    r = csv.reader(f)
    for row in r:
        movieID = int(row[0])
        movie_title = row[2]
        try:
            movie_index = movie_indices.index(movieID)
            title_to_index[movie_title] = movie_index
        except ValueError:
            pass
os.remove('individual_recommender\\title_to_index.pickle')
with open("individual_recommender\\title_to_index.pickle", "wb") as file:
    pickle.dump(title_to_index, file)
