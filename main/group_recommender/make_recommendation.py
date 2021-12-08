import os
import csv
import pandas as pd

print("Please enter the name of the file that houses the dataset:")
file_name = input()

try:
    os.chdir(os.getcwd().replace('\\group_recommender', ''))
    df_data = pd.read_csv('dataset\\' + file_name)
    df_data.index = df_data.iloc[:, 0]
    df_data = df_data.drop(df_data.columns[0], axis=1)
    data = df_data.values

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

    no_movies = len(data)
    sums = [0]*no_movies
    for row_index in range(no_movies):
        sums[row_index] = sum(data[row_index])

    largest_sum_value = max(sums)
    largest_sum_index = sums.index(largest_sum_value)
    for movie_title in title_to_index.keys():
        if title_to_index.get(movie_title) == largest_sum_index:
            top_recommended_movie_title = movie_title
            break
    print(f"The group's top recommended movie is titled '{top_recommended_movie_title}' as it is the movie that is most"
          f" liked by the group as a whole.")
except FileNotFoundError:
    print(f"There exists no file named '{file_name}'. Next time please enter the name of a file that does exist.")
