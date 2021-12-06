import csv
import pandas as pd

print("Please enter the name of the file that houses the dataset:")
input_movie = input()

try:
    df_data = pd.read_csv(input_movie)
    df_data.index = df_data.iloc[:, 0]
    df_data.index.name = "userID"
    df_data = df_data.drop(df_data.columns[0], axis=1)
    df_data.columns.name = "movieID"
    df_data = df_data.transpose()
    data = df_data.values

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

    no_movies = len(data)
    sums = [0]*no_movies
    for row_index in range(no_movies):
        sums[row_index] = sum(data[row_index])

    no_recommendations = 10
    print(f"Top {no_recommendations} recommendations:")
    for i in range(no_recommendations):
        largest_sum_value = max(sums)
        largest_sum_index = sums.index(largest_sum_value)
        sums[largest_sum_index] = 0
        for movie_title in title_to_index.keys():
            if title_to_index.get(movie_title) == largest_sum_index:
                break
        print(f"#{i+1}: '{movie_title}' with sum {largest_sum_value}")
except FileNotFoundError:
    print("Error: file does not exist")
